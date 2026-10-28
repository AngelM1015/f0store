# F0Store

F0Store is axi0's store of free and open-source Android apps. It installs and updates apps from repositories in the
F-Droid format: the two big community repositories and our own, ready from the first start, plus the
"axi0 picks" shelf: one free app for each everyday Google app ([PICKS.md](PICKS.md)).

FOSS only: every app in the repositories F0Store ships with is free and open-source software, shown with its own
licence and with the anti-features its repository marks. F0Store never offers apps copied out of Google Play.

F0Store runs on Android 6.0 and newer. It will be the preinstalled store of FluxOS for phones.

Download: https://axi0.tech/f0store (APK with its SHA-256 and signing certificate), or add our repository to any
F-Droid-compatible client: `https://axi0.tech/f0store/repo` with the fingerprint below.

## Based on Droid-ify

F0Store is a modified version of [Droid-ify](https://github.com/Droid-ify/client) 0.7.8 (GPL-3.0), which is based
on [Foxy Droid](https://github.com/kitsunyan/foxy-droid). The full history of both is kept in this repository. What
we changed, and when, is in [NOTICE.md](NOTICE.md). Thank you to the Droid-ify and Foxy Droid authors.

## Repositories it ships with

| Repository | Address | Enabled |
|---|---|---|
| F-Droid | `https://f-droid.org/repo` | yes |
| IzzyOnDroid | `https://apt.izzysoft.de/fdroid/repo` | yes |
| F0Store (ours) | `https://axi0.tech/f0store/repo` | yes |
| F-Droid Archive | `https://f-droid.org/archive` | off |

Any other repository can be added by its link or QR code, as in Droid-ify.

Apps in our repository besides F0Store itself: axi0 Photo Sync (`tech.axi0.photosync`, built in
https://github.com/AngelM1015/axi0-photo-sync), 0daylife, the Flux0S launcher (`tech.axi0.daylife`, built in
https://github.com/AngelM1015/0daylife) and axi0, the suite's applets as an app (`tech.axi0.suite`, built in
https://github.com/AngelM1015/axi0-android on Native Alpha, with its source tarball next to each APK), all signed with
the F0Store APK key. Each app's CI puts its APK and a
`<package>.latest` line into the repository directory; the publish job here lists the newest one in the signed index.

## What the app sends, and to whom

- To each enabled repository (or to one of the mirrors that repository lists): ordinary HTTPS requests for
  its signed index, app icons and screenshots, and the APK files you choose to install. Like any web request these
  carry your IP address and the HTTP client's default user agent. No account, no identifier, no list of your apps.
- To IzzyOnDroid, with the setting "reproducible builds" on (the default): its public reproducible-build log, so
  F0Store can show which of its apps are verified builds.
- Download statistics (IzzyOnDroid's public counts, `dlstats.izzyondroid.org`) are OFF in F0Store unless you turn
  them on in the settings.
- No analytics, no crash reporting, no advertising library. Links you tap (source code, licence, donation, the
  privacy-report buttons) open in your browser.

## Keys

| What | SHA-256 of the signing certificate |
|---|---|
| F0Store APK | `75920807E60E2896C2F9DD3799FA3C26BAAC7A66C0E72311E94EF469C315DE31` |
| F0Store repository index | `F6C7C97F6DB494B837FB2633FA8F744DB935E8D5DAC65BBFC79E4855CD031205` |

Check an APK with `apksigner verify --print-certs F0Store-<version>.apk`.

## Build

Builds, signing, emulator tests and the repository publish all run in GitHub Actions (`.github/workflows/f0store.yml`):

1. `python3 tools/picks.py --check` (the picks list in the app matches `docs/picks.json`),
2. `./gradlew assembleRelease`, signed with the F0Store key held in the repository's Actions secrets,
3. an Android emulator test (`tests/emulator.sh`, Maestro flows in `tests/flows/`): install F0Store, sync the three
   repositories, browse, search, install a pick, update an app; screenshots are kept as a workflow artifact,
4. on a manual run with `publish`, the signed APK goes into our repository (`repo/`, built with fdroidserver,
   index signed with the repository key) at `https://axi0.tech/f0store/repo`.

Locally: `./gradlew assembleDebug` with JDK 17 and the Android SDK, as for Droid-ify.

## Licence

GPL-3.0, see [LICENSE](LICENSE). Copyright of the Droid-ify and Foxy Droid code stays with their authors; the
changes listed in NOTICE.md are Copyright 2026 axi0, under the same licence. App metadata shown inside F0Store comes
from each repository under that repository's and that app's own licences ([TERMS.md](TERMS.md)).
