#!/bin/bash
# build.sh <signed F0Store apk> <versionCode> <work dir>   (CI) the F0Store repository in F-Droid format.
# Keeps every APK the live repository already lists, adds the new one as tech.axi0.f0store_<code>.apk, writes the
# metadata and lets fdroidserver build index-v1 and index-v2 and sign them (entry.jar, index-v1.jar) with the
# repository key from the environment (REPO_P12_B64, REPO_PASS). Checks the index signer is the F0Store repo key.
set -euo pipefail
apk=$(cd "$(dirname "$1")" && pwd)/$(basename "$1") code=$2 work=$3   # absolute: we cd into the work dir
here=$(cd "$(dirname "$0")" && pwd)
WANT=F6C7C97F6DB494B837FB2633FA8F744DB935E8D5DAC65BBFC79E4855CD031205
LIVE=https://axi0.tech/f0store/repo
mkdir -p "$work/repo" "$work/metadata" && cd "$work"
umask 077
printf %s "$REPO_P12_B64" | base64 -d > keystore.p12
KS_PASS=$(printf %s "$REPO_PASS" | tr -d '\r\n'); export KS_PASS
keytool -list -storetype PKCS12 -keystore keystore.p12 -storepass:env KS_PASS -alias f0store-repo >/dev/null \
  || { echo "keytool cannot read the repository keystore" >&2; exit 1; }
umask 022
# What the live repository lists stays listed (older F0Store versions remain installable and verifiable).
if curl -fsS "$LIVE/index-v1.json" -o live-v1.json 2>/dev/null; then
  python3 - "$LIVE" <<'EOF'
import json, sys, urllib.request
live = sys.argv[1]
for pkgs in json.load(open('live-v1.json')).get('packages', {}).values():
    for p in pkgs:
        name = p['apkName']
        urllib.request.urlretrieve(f'{live}/{name}', f'repo/{name}')
        print('kept', name)
EOF
fi
cp "$apk" "repo/tech.axi0.f0store_${code}.apk"
cp -R "$here/metadata/." metadata/
# Our icon wherever fdroidserver looks for repo_icon, so it never falls back to its own placeholder artwork.
mkdir -p repo/icons && cp "$here/icon.png" repo/icons/icon.png && cp "$here/icon.png" icon.png
cat > config.yml <<EOF
repo_url: $LIVE
repo_name: F0Store
repo_description: >-
  axi0's own repository of free and open-source Android apps: F0Store itself, and the axi0 apps for Android as they
  come. Every APK is built in public CI from https://github.com/AngelM1015/f0store and signed by axi0.
repo_icon: icon.png
archive_older: 0
repo_keyalias: f0store-repo
keystore: keystore.p12
keystorepass: {env: KS_PASS}
keypass: {env: KS_PASS}
keydname: CN=F0Store repository, O=axi0
sdk_path: $ANDROID_HOME
make_current_version_link: false
EOF
chmod 600 config.yml
fdroid update --verbose 2>&1 | grep -vE 'keystorepass|keypass' | tail -40
for f in entry.jar entry.json index-v1.jar index-v1.json index-v2.json; do [ -s "repo/$f" ] || { echo "missing repo/$f" >&2; exit 1; }; done
got=$(keytool -printcert -jarfile repo/entry.jar | grep -m1 -E 'SHA256:' | sed 's/.*SHA256: //; s/://g' | tr a-f A-F)
[ "$got" = "$WANT" ] || { echo "entry.jar signed by $got, not the F0Store repository key" >&2; exit 1; }
echo "index signer SHA-256 $got"
rm -f keystore.p12
python3 -c "import json; d=json.load(open('repo/index-v2.json')); print('repo icon:', d['repo'].get('icon')); p=d['packages']['tech.axi0.f0store']; print('index-v2:', len(d['packages']), 'package(s);', 'F0Store versions:', sorted(v['manifest']['versionCode'] for v in p['versions'].values()))"
ls -la repo
