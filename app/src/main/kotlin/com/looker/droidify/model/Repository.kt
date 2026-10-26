package com.looker.droidify.model

import java.net.URL

data class Repository(
    var id: Long,
    val address: String,
    val mirrors: List<String>,
    val name: String,
    val description: String,
    val version: Int,
    val enabled: Boolean,
    val fingerprint: String,
    val lastModified: String,
    val entityTag: String,
    val updated: Long,
    val timestamp: Long,
    val authentication: String,
) {

    fun edit(address: String, fingerprint: String, authentication: String): Repository {
        val isAddressChanged = this.address != address
        val isFingerprintChanged = this.fingerprint != fingerprint
        val shouldForceUpdate = isAddressChanged || isFingerprintChanged
        return copy(
            address = address,
            fingerprint = fingerprint,
            lastModified = if (shouldForceUpdate) "" else lastModified,
            entityTag = if (shouldForceUpdate) "" else entityTag,
            authentication = authentication,
        )
    }

    fun update(
        mirrors: List<String>,
        name: String,
        description: String,
        version: Int,
        lastModified: String,
        entityTag: String,
        timestamp: Long,
    ): Repository {
        return copy(
            mirrors = mirrors,
            name = name,
            description = description,
            version = if (version >= 0) version else this.version,
            lastModified = lastModified,
            entityTag = entityTag,
            updated = System.currentTimeMillis(),
            timestamp = timestamp,
        )
    }

    fun enable(enabled: Boolean): Repository {
        return copy(enabled = enabled, lastModified = "", entityTag = "")
    }

    @Suppress("SpellCheckingInspection")
    companion object {

        fun newRepository(
            address: String,
            fingerprint: String,
            authentication: String,
        ): Repository {
            val name = try {
                URL(address).let { "${it.host}${it.path}" }
            } catch (e: Exception) {
                address
            }
            return defaultRepository(address, name, "", 0, true, fingerprint, authentication)
        }

        fun defaultRepository(
            address: String,
            name: String,
            description: String,
            version: Int = 21,
            enabled: Boolean = false,
            fingerprint: String,
            authentication: String = "",
        ): Repository {
            return Repository(
                -1, address, emptyList(), name, description, version, enabled,
                fingerprint, "", "", 0L, 0L, authentication,
            )
        }

        // F0Store: the community repositories we ship with, then our own. Others can be added by link.
        val defaultRepositories = listOf(
            defaultRepository(
                address = "https://f-droid.org/repo",
                name = "F-Droid",
                description = "The official F-Droid Free Software repos" +
                    "itory. Everything in this repository is always buil" +
                    "t from the source code.",
                enabled = true,
                fingerprint = "43238D512C1E5EB2D6569F4A3AFBF5523418B82E0A3ED1552770ABB9A9C9CCAB",
            ),
            defaultRepository(
                address = "https://f-droid.org/archive",
                name = "F-Droid Archive",
                description = "The archive of the official F-Droid Free" +
                    " Software repository. Apps here are old and can co" +
                    "ntain known vulnerabilities and security issues!",
                fingerprint = "43238D512C1E5EB2D6569F4A3AFBF5523418B82E0A3ED1552770ABB9A9C9CCAB",
            ),
            defaultRepository(
                address = "https://apt.izzysoft.de/fdroid/repo",
                name = "IzzyOnDroid F-Droid repository",
                description = "This is a repository of apps to be used with" +
                    " F-Droid the original application developers, taken" +
                    " from the responsible repositories. At thi" +
                    "s moment I cannot give guarantees on regular updates" +
                    " for all of them, though most are checked multiple times a week.",
                enabled = true,
                fingerprint = "3BF0D6ABFEAE2F401707B6D966BE743BF0EEE49C2561B9BA39073711F628937A",
            ),
            defaultRepository(
                address = "https://axi0.tech/f0store/repo",
                name = "F0Store",
                description = "axi0's own repository: F0Store itself and the axi0 apps " +
                    "for Android as they come. Signed by axi0.",
                enabled = true,
                fingerprint = "F6C7C97F6DB494B837FB2633FA8F744DB935E8D5DAC65BBFC79E4855CD031205",
            ),
        )

        fun newRepos(): List<Repository> = listOf()

        fun addressesToRemove(): List<String> = listOf(
            // Add repository addresses that should be removed during database upgrades and remove them from the lists above
            // Example: "https://example.com/fdroid/repo"
        )
    }
}
