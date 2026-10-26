#!/bin/bash
# selfupdate.sh <screenshot dir>   (CI, after a publish, on a booted emulator)
# F0Store updates itself: install the previous F0Store from the live repository, let it sync, update it from its own
# Updates tab. The result comes from the package manager (versionCode), not from the screen.
set -uo pipefail
root=$(pwd)
out=$(mkdir -p "$1" && cd "$1" && pwd)
pkg=tech.axi0.f0store
tmp=$(mktemp -d); touch "$tmp/stamp"
vc() { adb shell dumpsys package "$1" | grep -m1 -oE 'versionCode=[0-9]+' | cut -d= -f2; }
read -r prev newest < <(curl -fsS https://axi0.tech/f0store/repo/index-v2.json | python3 -c '
import json, sys
v = sorted(x["manifest"]["versionCode"] for x in json.load(sys.stdin)["packages"]["tech.axi0.f0store"]["versions"].values())
print(v[-2] if len(v) > 1 else 0, v[-1])')
[ "${prev:-0}" -gt 0 ] || { echo "SKIP self-update: one F0Store version in the repository"; exit 0; }
curl -fsSL -o "$tmp/prev.apk" "https://axi0.tech/f0store/repo/tech.axi0.f0store_${prev}.apk"
adb wait-for-device
adb install "$tmp/prev.apk" || { echo "FAIL install F0Store $prev"; exit 1; }
adb shell appops set $pkg REQUEST_INSTALL_PACKAGES allow
adb shell pm grant $pkg android.permission.POST_NOTIFICATIONS 2>/dev/null || true
echo "F0Store $(vc $pkg) installed from the live repository; newest there: $newest"
(cd "$out" && maestro test "$root/tests/flows/06-self-update.yaml"); rc=$?
for _ in $(seq 1 60); do [ "$(vc $pkg)" = "$newest" ] && break; sleep 2; done
adb exec-out screencap -p > "$out/06-end.png" 2>/dev/null || true
find "$root/tests" "$HOME/.maestro" "$out" -name '06[a-z]-*.png' -newer "$tmp/stamp" -exec cp -n {} "$out/" \; 2>/dev/null || true
after=$(vc $pkg)
adb shell dumpsys package $pkg | grep -m1 -oE 'installerPackageName=[^ ]+' || true
rm -rf "$tmp"
if [ "$after" = "$newest" ]; then echo "PASS self-update through F0Store: $prev -> $after"; exit 0; fi
echo "FAIL self-update: $prev -> ${after:-none} (flow rc $rc)"
adb shell uiautomator dump /sdcard/ui.xml >/dev/null 2>&1 && adb pull /sdcard/ui.xml "$out/06-fail.xml" >/dev/null 2>&1
exit 1
