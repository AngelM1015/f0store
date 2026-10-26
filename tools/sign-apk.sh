#!/bin/bash
# sign-apk.sh <unsigned.apk> <out.apk>   (CI) sign with the F0Store key and prove it is that key.
# The key comes from the environment (P12_B64 = base64 PKCS#12, P12_PASS = its password), never from a file in the
# repository; it is written to a private temp dir that is removed on exit. Nothing secret is printed.
set -euo pipefail
in=$1 out=$2
WANT=75920807E60E2896C2F9DD3799FA3C26BAAC7A66C0E72311E94EF469C315DE31   # SHA-256 of the F0Store APK certificate
bt=$(ls -d "$ANDROID_HOME"/build-tools/* | sort -V | tail -1)
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT; chmod 700 "$tmp"
printf %s "$P12_B64" | base64 -d > "$tmp/in.p12"
KS_PASS=$(printf %s "$P12_PASS" | tr -d '\r\n'); export KS_PASS
# Java reads the PKCS#12 as exported (the classic PBE ciphers keytool itself used); re-wrap it with OpenSSL only if not.
ks="$tmp/in.p12"
if ! keytool -list -storetype PKCS12 -keystore "$ks" -storepass:env KS_PASS -alias f0store >/dev/null 2>&1; then
  echo "keytool cannot read the keystore as exported; re-wrapping with openssl" >&2
  openssl pkcs12 -legacy -in "$ks" -passin env:KS_PASS -nodes | openssl pkcs12 -export -name f0store -passout env:KS_PASS -out "$tmp/apk.p12"
  ks="$tmp/apk.p12"
fi
mkdir -p "$(dirname "$out")"
"$bt/zipalign" -c -p 4 "$in" >/dev/null 2>&1 || { "$bt/zipalign" -p -f 4 "$in" "$tmp/aligned.apk"; in="$tmp/aligned.apk"; }
"$bt/apksigner" sign --ks "$ks" --ks-type PKCS12 --ks-pass env:KS_PASS --key-pass env:KS_PASS \
  --ks-key-alias f0store --out "$out" "$in"
got=$("$bt/apksigner" verify --print-certs "$out" | grep -m1 'certificate SHA-256 digest' | awk '{print toupper($NF)}')
[ "$got" = "$WANT" ] || { echo "signed by $got, not the F0Store key" >&2; exit 1; }
"$bt/apksigner" verify --verbose "$out" | grep -E '^Verified using v[0-9]'
echo "signer SHA-256 $got"
sha256sum "$out" | tee "$out.sha256"
