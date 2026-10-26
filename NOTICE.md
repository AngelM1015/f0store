# Notice of modification (GPL-3.0, section 5a)

F0Store is a modified version of Droid-ify 0.7.8 (https://github.com/Droid-ify/client, tag v0.7.8, commit
ff1453ed957f), modified by axi0 starting on 2026-10-25. The upstream history is kept in full.

## Changes

2026-10-25, F0Store 0.1.0:
- Name and identity: app name F0Store, application id `tech.axi0.f0store`, version 0.1.0 (code 1). The Kotlin
  package names stay upstream's (`com.looker.droidify`) so upstream fixes keep merging.
- Icon: our own (black tile, white bag, one orange dot), adaptive with a monochrome layer; the Droid-ify artwork
  is removed from this fork.
- Colours: the Material 3 scheme is generated from axi0's orange (#f6a04d) for light, dark and the two contrast
  levels; Material You (dynamic colour) is on by default.
- Default repositories: F-Droid, IzzyOnDroid and the F0Store repository enabled, the F-Droid archive offered off;
  the other upstream presets are removed (any repository can still be added by link).
- "axi0 picks": a new section, the default shelf of the Explore tab, listing `docs/picks.json` (the register is
  PICKS.md); a search from it searches every app.
- Privacy defaults: IzzyOnDroid download statistics off by default.
- The Play Store and APKMirror shortcut-button presets are removed (F0Store never points at Play builds).
- Credits in the settings: F0Store's source first, then Droid-ify and Foxy Droid.
- Upstream's CI, release script, issue templates, store listing and README artwork are replaced by ours.

2026-10-26, F0Store 0.1.1:
- App pages open with the Links section expanded, so each app's licence shows without a tap.
- The axi0 picks list starts on the picks section (upstream's list default was All apps).
