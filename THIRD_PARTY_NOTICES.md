# Third-party notices: f0store

What this repository ships or runs that other people wrote, with each licence. Our own code is the axi0 team's and is not listed here. The README's "Built on" section says the same in prose.

Generated 2026-10-28 by `third-party-notices.mjs` (axi0-network, `scripts/`) from the Android build files. The tables "Taken projects", "Vendored folders" (project, version, licence, link) and "Android libraries" are kept by hand; the package and crate tables are rebuilt on every run.

## Taken projects

| Project | Version | Licence | Link | How we take it | Our part |
|---|---|---|---|---|---|
| Droid-ify | 0.7.8 (commit ff1453ed957f) | GPL-3.0 | https://github.com/Droid-ify/client | forked: the whole client (NOTICE.md dates every change) | the F0Store shelf, picks, our repository, store rules (TERMS.md) |
| F-Droid and IzzyOnDroid repositories | - | their terms (TERMS.md) | https://f-droid.org/ | the app catalogues it reads | - |

## Android libraries

Declared in the Gradle build files; each brings its own dependencies, which the APK carries too.

| Library | Version | Licence | Link | Shipped |
|---|---|---|---|---|
| com.google.android.material:material | 1.14.0 | Apache-2.0 | https://github.com/material-components/material-components-android | yes |
| androidx.activity:activity | 1.13.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.fragment:fragment-ktx | 1.9.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.appcompat:appcompat | 1.8.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.core:core-ktx | 1.19.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.datastore:datastore-preferences | 1.2.1 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.datastore:datastore | 1.2.1 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.lifecycle:lifecycle-runtime | 2.11.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.lifecycle:lifecycle-viewmodel | 2.11.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.recyclerview:recyclerview | 1.4.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.sqlite:sqlite-ktx | 2.7.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.test.ext:junit-ktx | 1.3.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | tests or debug only |
| androidx.test:rules | 1.7.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | tests or debug only |
| androidx.test:runner | 1.7.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | tests or debug only |
| androidx.test:core | 1.7.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | tests or debug only |
| androidx.test:core-ktx | 1.7.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | tests or debug only |
| androidx.work:work-runtime-ktx | 2.11.2 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| io.coil-kt.coil3:coil | 3.6.2 | Apache-2.0 | https://github.com/coil-kt/coil | yes |
| io.coil-kt.coil3:coil-compose | 3.6.2 | Apache-2.0 | https://github.com/coil-kt/coil | yes |
| io.coil-kt.coil3:coil-network-okhttp | 3.6.2 | Apache-2.0 | https://github.com/coil-kt/coil | yes |
| com.google.dagger:hilt-core | 2.60.1 | Apache-2.0 | https://github.com/google/dagger | yes |
| com.google.dagger:hilt-android | 2.60.1 | Apache-2.0 | https://github.com/google/dagger | yes |
| com.google.dagger:hilt-android-testing | 2.60.1 | Apache-2.0 | https://github.com/google/dagger | tests or debug only |
| com.google.dagger:hilt-android-compiler | 2.60.1 | Apache-2.0 | https://github.com/google/dagger | yes |
| androidx.hilt:hilt-work | 1.4.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.hilt:hilt-compiler | 1.4.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| com.squareup.leakcanary:leakcanary-android | 2.14 | Apache-2.0 | https://github.com/square/leakcanary | tests or debug only |
| com.fasterxml.jackson.core:jackson-core | 2.22.2 | Apache-2.0 | https://github.com/FasterXML/jackson-core | yes |
| org.jetbrains.kotlin:kotlin-stdlib | 2.4.20 | Apache-2.0 | https://github.com/JetBrains/kotlin | yes |
| org.jetbrains.kotlin:kotlin-test | 2.4.20 | Apache-2.0 | https://github.com/JetBrains/kotlin | tests or debug only |
| org.jetbrains.kotlin:kotlin-test-junit5 | 2.4.20 | Apache-2.0 | https://github.com/JetBrains/kotlin | tests or debug only |
| org.jetbrains.kotlinx:kotlinx-coroutines-core | 1.11.0 | Apache-2.0 | https://github.com/Kotlin | yes |
| org.jetbrains.kotlinx:kotlinx-coroutines-android | 1.11.0 | Apache-2.0 | https://github.com/Kotlin | yes |
| org.jetbrains.kotlinx:kotlinx-coroutines-guava | 1.11.0 | Apache-2.0 | https://github.com/Kotlin | yes |
| org.jetbrains.kotlinx:kotlinx-coroutines-test | 1.11.0 | Apache-2.0 | https://github.com/Kotlin | tests or debug only |
| org.jetbrains.kotlinx:kotlinx-serialization-json | 1.11.0 | Apache-2.0 | https://github.com/Kotlin | yes |
| com.squareup.okhttp3:okhttp | 5.5.0 | Apache-2.0 | https://github.com/square/okhttp | yes |
| com.squareup.okhttp3:mockwebserver3 | 5.5.0 | Apache-2.0 | https://github.com/square/okhttp | yes |
| com.github.topjohnwu.libsu:core | 6.0.0 | Apache-2.0 | https://github.com/topjohnwu/libsu | yes |
| androidx.room:room-compiler | 2.8.4 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.room:room-ktx | 2.8.4 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.room:room-runtime | 2.8.4 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.room:room-testing | 2.8.4 | Apache-2.0 | https://developer.android.com/jetpack/androidx | tests or debug only |
| dev.rikka.shizuku:api | 13.0.0 | MIT | https://github.com/RikkaApps/Shizuku-API | yes |
| dev.rikka.shizuku:provider | 13.0.0 | MIT | https://github.com/RikkaApps/Shizuku-API | yes |
| com.github.stfalcon-studio:StfalconImageViewer | 1.0.1 | Apache-2.0 | https://github.com/stfalcon-studio/StfalconImageViewer | yes |
| org.junit:junit-bom | 6.1.3 | EPL-2.0 | https://github.com/junit-team/junit5 | tests or debug only |
| org.junit.jupiter:junit-jupiter | BOM | EPL-2.0 | https://github.com/junit-team/junit5 | tests or debug only |
| org.junit.platform:junit-platform-launcher | BOM | EPL-2.0 | https://github.com/junit-team/junit5 | tests or debug only |
| org.robolectric:robolectric | 4.16.1 | MIT | https://github.com/robolectric/robolectric | tests or debug only |
| androidx.arch.core:core-testing | 2.2.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | tests or debug only |
| io.mockk:mockk | 1.14.11 | Apache-2.0 | https://github.com/mockk/mockk | tests or debug only |
| io.mockk:mockk-android | 1.14.11 | Apache-2.0 | https://github.com/mockk/mockk | tests or debug only |
| app.cash.turbine:turbine | 1.2.1 | Apache-2.0 | https://github.com/cashapp/turbine | tests or debug only |
| org.junit.vintage:junit-vintage-engine | BOM | EPL-2.0 | https://github.com/junit-team/junit5 | tests or debug only |
| com.github.T8RIN.QuickieExtended:quickie-foss | 1.18.1 | MIT | https://github.com/T8RIN/QuickieExtended | yes |
| com.android.tools:desugar_jdk_libs | 2.1.5 | GPL-2.0 with Classpath Exception | https://github.com/google/desugar_jdk_libs | yes |
| androidx.compose:compose-bom | 2026.02.00 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.compose.ui:ui | BOM | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.compose.ui:ui-graphics | BOM | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.compose.ui:ui-tooling | BOM | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.compose.ui:ui-tooling-preview | BOM | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.compose.ui:ui-test-manifest | BOM | Apache-2.0 | https://developer.android.com/jetpack/androidx | tests or debug only |
| androidx.compose.material3:material3 | 1.5.0-alpha15 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.activity:activity-compose | 1.13.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.navigation:navigation-compose | 2.9.7 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.hilt:hilt-navigation-compose | 1.4.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |
| androidx.lifecycle:lifecycle-viewmodel-compose | 2.11.0 | Apache-2.0 | https://developer.android.com/jetpack/androidx | yes |

## Licences counted

Rows per licence in the tables above (vendored folders, packages, crates, libraries).

Apache-2.0: 59; MIT: 4; EPL-2.0: 4; GPL-2.0 with Classpath Exception: 1

## Where the licence texts are

- Vendored folders: the files named in their row, inside the folder.
- npm packages and Rust crates: each package's own licence file, inside its published archive (the link on its name).
