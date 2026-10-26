#!/bin/bash
# emulator.sh <apk dir> <screenshot dir>   (CI, on a booted emulator)
# End to end: install F0Store, let it sync its three repositories, browse, search, install a pick (Open Camera) and
# update an app (an older F-Droid build of Markor installed first). A screenshot after every flow, the flows' own
# screenshots, and a UI dump when a flow fails. The last checks ask the package manager, not the screen.
set -uo pipefail
root=$(pwd)
apk=$(ls "$1"/F0Store-*.apk | head -1)
out=$(mkdir -p "$2" && cd "$2" && pwd)
pkg=tech.axi0.f0store
fail=0
tmp=$(mktemp -d)
shot() { adb exec-out screencap -p > "$out/$1.png" 2>/dev/null || true; }
dump() { adb shell uiautomator dump /sdcard/ui.xml >/dev/null 2>&1 && adb pull /sdcard/ui.xml "$out/$1.xml" >/dev/null 2>&1 || true; }
vc() { adb shell dumpsys package "$1" | grep -m1 -oE 'versionCode=[0-9]+' | cut -d= -f2; }
step() {   # step <name>: run tests/flows/<name>.yaml from the screenshot dir (takeScreenshot writes there)
  echo "== $1"
  if (cd "$out" && maestro test "$root/tests/flows/$1.yaml"); then echo "PASS $1"; else echo "FAIL $1"; fail=1; dump "$1-fail"; fi
  shot "$1-end"
}

adb wait-for-device
echo "device: API $(adb shell getprop ro.build.version.sdk | tr -d '\r'), $(adb shell getprop ro.product.cpu.abi | tr -d '\r')"
adb install -r "$apk" || { echo "FAIL install F0Store"; exit 1; }
echo "PASS install F0Store $(vc $pkg) ($(basename "$apk"))"
adb shell appops set $pkg REQUEST_INSTALL_PACKAGES allow
adb shell pm grant $pkg android.permission.POST_NOTIFICATIONS 2>/dev/null || true

# The update target: the oldest Markor build the F-Droid repository still serves (same signer as the newest).
old=$(curl -fsS https://f-droid.org/api/v1/packages/net.gsantner.markor \
  | python3 -c 'import json,sys; print(min(p["versionCode"] for p in json.load(sys.stdin)["packages"]))')
curl -fsSL -o "$tmp/markor-old.apk" "https://f-droid.org/repo/net.gsantner.markor_${old}.apk"
adb install "$tmp/markor-old.apk" >/dev/null || { echo "FAIL install old Markor"; exit 1; }
before=$(vc net.gsantner.markor)
echo "Markor installed at versionCode $before (to be updated from F0Store)"

for f in 01-start-sync 02-browse 03-search 04-install-pick 05-update; do step $f; done

if adb shell pm list packages net.sourceforge.opencamera | grep -q opencamera; then
  echo "PASS pick installed through F0Store: Open Camera versionCode $(vc net.sourceforge.opencamera)"
else
  echo "FAIL pick not installed"; fail=1
fi
after=$(vc net.gsantner.markor)
if [ "${after:-0}" -gt "${before:-0}" ]; then echo "PASS update through F0Store: Markor $before -> $after"
else echo "FAIL update: Markor $before -> ${after:-none}"; fail=1; fi
adb shell dumpsys package net.gsantner.markor | grep -m1 -oE 'installerPackageName=[^ ]+' || true
adb logcat -d -t 3000 > "$out/logcat.txt" 2>/dev/null || true
rm -rf "$tmp"
echo "result: $([ $fail = 0 ] && echo PASS || echo FAIL)"
exit $fail
