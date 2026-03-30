"""
composeforge.templates.gradle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Gradle build file templates: version catalog, root/app build.gradle.kts, settings.
"""

from composeforge.core.config import ProjectConfig


def version_catalog(libs: list) -> str:
    """Génère gradle/libs.versions.toml."""
    V, L, P = "", "", ""

    V += """\
[versions]
agp                = "8.7.3"
kotlin             = "2.1.0"
coreKtx            = "1.15.0"
lifecycle          = "2.8.7"
activityCompose    = "1.9.3"
composeBom         = "2024.12.01"
junit              = "4.13.2"
junitExt           = "1.2.1"
espresso           = "3.6.1"
splashscreen       = "1.0.1"
timber             = "5.0.1"
"""
    L += """\
[libraries]
kotlin-bom                       = { group = "org.jetbrains.kotlin",    name = "kotlin-bom",               version.ref = "kotlin"          }
androidx-core-ktx                = { group = "androidx.core",            name = "core-ktx",                 version.ref = "coreKtx"         }
androidx-lifecycle-runtime-ktx   = { group = "androidx.lifecycle",       name = "lifecycle-runtime-ktx",    version.ref = "lifecycle"        }
androidx-lifecycle-compose       = { group = "androidx.lifecycle",       name = "lifecycle-runtime-compose", version.ref = "lifecycle"       }
androidx-activity-compose        = { group = "androidx.activity",        name = "activity-compose",         version.ref = "activityCompose"  }
androidx-compose-bom             = { group = "androidx.compose",         name = "compose-bom",              version.ref = "composeBom"       }
androidx-ui                      = { group = "androidx.compose.ui",      name = "ui"                                                         }
androidx-ui-graphics             = { group = "androidx.compose.ui",      name = "ui-graphics"                                                }
androidx-ui-tooling              = { group = "androidx.compose.ui",      name = "ui-tooling"                                                 }
androidx-ui-tooling-preview      = { group = "androidx.compose.ui",      name = "ui-tooling-preview"                                         }
androidx-material3               = { group = "androidx.compose.material3", name = "material3"                                                }
junit                            = { group = "junit",                    name = "junit",                    version.ref = "junit"            }
androidx-junit                   = { group = "androidx.test.ext",        name = "junit",                    version.ref = "junitExt"         }
androidx-espresso-core           = { group = "androidx.test.espresso",   name = "espresso-core",            version.ref = "espresso"         }
androidx-ui-test-manifest        = { group = "androidx.compose.ui",      name = "ui-test-manifest"                                           }
androidx-ui-test-junit4          = { group = "androidx.compose.ui",      name = "ui-test-junit4"                                             }
androidx-splashscreen            = { group = "androidx.core",            name = "core-splashscreen",        version.ref = "splashscreen"     }
timber                           = { group = "com.jakewharton.timber",   name = "timber",                   version.ref = "timber"           }
"""
    P += """\
[plugins]
android-application = { id = "com.android.application",       version.ref = "agp"    }
kotlin-android      = { id = "org.jetbrains.kotlin.android",  version.ref = "kotlin" }
kotlin-compose      = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
"""

    if "Hilt" in libs:
        V += 'hilt               = "2.56.2"\n'
        V += 'ksp                = "2.1.0-1.0.29"\n'
        L += 'hilt-android           = { group = "com.google.dagger", name = "hilt-android",          version.ref = "hilt" }\n'
        L += 'hilt-compiler          = { group = "com.google.dagger", name = "hilt-android-compiler",  version.ref = "hilt" }\n'
        L += 'hilt-navigation-compose = { group = "androidx.hilt",   name = "hilt-navigation-compose", version = "1.2.0"    }\n'
        P += 'hilt                = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }\n'
        P += 'ksp                 = { id = "com.google.devtools.ksp", version.ref = "ksp" }\n'

    if "Retrofit" in libs:
        V += 'retrofit           = "2.11.0"\n'
        V += 'okhttp             = "4.12.0"\n'
        L += 'retrofit                = { group = "com.squareup.retrofit2", name = "retrofit",             version.ref = "retrofit" }\n'
        L += 'retrofit-gson           = { group = "com.squareup.retrofit2", name = "converter-gson",       version.ref = "retrofit" }\n'
        L += 'okhttp                  = { group = "com.squareup.okhttp3",   name = "okhttp",               version.ref = "okhttp"   }\n'
        L += 'okhttp-logging          = { group = "com.squareup.okhttp3",   name = "logging-interceptor",  version.ref = "okhttp"   }\n'

    if "Navigation" in libs:
        V += 'navigationCompose  = "2.8.5"\n'
        L += 'navigation-compose      = { group = "androidx.navigation", name = "navigation-compose", version.ref = "navigationCompose" }\n'

    if "Coil" in libs:
        V += 'coil               = "2.7.0"\n'
        L += 'coil-compose            = { group = "io.coil-kt", name = "coil-compose", version.ref = "coil" }\n'

    if "Coroutines" in libs:
        V += 'coroutines         = "1.9.0"\n'
        L += 'coroutines-android      = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-android", version.ref = "coroutines" }\n'
        L += 'coroutines-core         = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-core",    version.ref = "coroutines" }\n'

    if "DataStore" in libs:
        V += 'datastore          = "1.1.2"\n'
        L += 'datastore-preferences   = { group = "androidx.datastore", name = "datastore-preferences", version.ref = "datastore" }\n'

    if "Room" in libs:
        V += 'room               = "2.6.1"\n'
        if "Hilt" not in libs:
            V += 'ksp                = "2.1.0-1.0.29"\n'
        L += 'room-runtime            = { group = "androidx.room", name = "room-runtime", version.ref = "room" }\n'
        L += 'room-ktx                = { group = "androidx.room", name = "room-ktx",     version.ref = "room" }\n'
        L += 'room-compiler           = { group = "androidx.room", name = "room-compiler", version.ref = "room" }\n'
        if "Hilt" not in libs:
            P += 'ksp                 = { id = "com.google.devtools.ksp", version.ref = "ksp" }\n'

    if "Ktor" in libs:
        V += 'ktor               = "3.0.3"\n'
        L += 'ktor-client-core                   = { group = "io.ktor", name = "ktor-client-core",                   version.ref = "ktor" }\n'
        L += 'ktor-client-android                = { group = "io.ktor", name = "ktor-client-android",                version.ref = "ktor" }\n'
        L += 'ktor-client-content-negotiation    = { group = "io.ktor", name = "ktor-client-content-negotiation",    version.ref = "ktor" }\n'
        L += 'ktor-serialization-kotlinx-json    = { group = "io.ktor", name = "ktor-serialization-kotlinx-json",   version.ref = "ktor" }\n'
        L += 'ktor-client-logging                = { group = "io.ktor", name = "ktor-client-logging",               version.ref = "ktor" }\n'

    return V + "\n" + L + "\n" + P


def root_gradle(libs: list | None = None) -> str:
    """Génère le build.gradle.kts racine."""
    if libs is None:
        libs = []
    extra = ""
    if "Hilt" in libs or "Room" in libs:
        extra += "    alias(libs.plugins.ksp)                 apply false\n"
    if "Hilt" in libs:
        extra += "    alias(libs.plugins.hilt)                apply false\n"
    return f"""\
// Top-level build file
plugins {{
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android)      apply false
    alias(libs.plugins.kotlin.compose)      apply false
{extra}}}
"""


def app_gradle(cfg: ProjectConfig) -> str:
    """Génère app/build.gradle.kts."""
    pkg, libs, min_sdk = cfg.package, cfg.libs, cfg.min_sdk

    pl = 'plugins {\n    alias(libs.plugins.android.application)\n    alias(libs.plugins.kotlin.android)\n    alias(libs.plugins.kotlin.compose)\n'
    if "Hilt" in libs:
        pl += '    alias(libs.plugins.hilt)\n    alias(libs.plugins.ksp)\n'
    if "Room" in libs and "Hilt" not in libs:
        pl += '    alias(libs.plugins.ksp)\n'
    pl += '}\n'

    an = f"""
android {{
    namespace   = "{pkg}"
    compileSdk  = 35

    defaultConfig {{
        applicationId           = "{pkg}"
        minSdk                  = {min_sdk}
        targetSdk               = 35
        versionCode             = 1
        versionName             = "1.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }}

    buildTypes {{
        release {{
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }}
    }}
    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }}
    buildFeatures {{
        compose = true
        buildConfig = true
    }}
}}

kotlin {{
    compilerOptions {{
        jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_11)
    }}
}}
"""

    dep = """
dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.lifecycle.compose)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.ui)
    implementation(libs.androidx.ui.graphics)
    implementation(libs.androidx.ui.tooling.preview)
    implementation(libs.androidx.material3)
    debugImplementation(libs.androidx.ui.tooling)
    implementation(libs.androidx.splashscreen)
    implementation(libs.timber)
"""
    if "Hilt" in libs:
        dep += "    implementation(libs.hilt.android)\n    ksp(libs.hilt.compiler)\n    implementation(libs.hilt.navigation.compose)\n"
    if "Retrofit" in libs:
        dep += "    implementation(libs.retrofit)\n    implementation(libs.retrofit.gson)\n    implementation(libs.okhttp)\n    implementation(libs.okhttp.logging)\n"
    if "Navigation" in libs:
        dep += "    implementation(libs.navigation.compose)\n"
    if "Coil" in libs:
        dep += "    implementation(libs.coil.compose)\n"
    if "Coroutines" in libs:
        dep += "    implementation(libs.coroutines.android)\n    implementation(libs.coroutines.core)\n"
    if "DataStore" in libs:
        dep += "    implementation(libs.datastore.preferences)\n"
    if "Room" in libs:
        dep += "    implementation(libs.room.runtime)\n    implementation(libs.room.ktx)\n    ksp(libs.room.compiler)\n"
    if "Ktor" in libs:
        dep += "    implementation(libs.ktor.client.core)\n    implementation(libs.ktor.client.android)\n    implementation(libs.ktor.client.content.negotiation)\n    implementation(libs.ktor.serialization.kotlinx.json)\n    implementation(libs.ktor.client.logging)\n"
    dep += "\n    // ── Tests ──\n"
    dep += "    testImplementation(libs.junit)\n"
    dep += "    androidTestImplementation(libs.androidx.junit)\n"
    dep += "    androidTestImplementation(libs.androidx.espresso.core)\n"
    dep += "    androidTestImplementation(platform(libs.androidx.compose.bom))\n"
    dep += "    androidTestImplementation(libs.androidx.ui.test.junit4)\n"
    dep += "    debugImplementation(libs.androidx.ui.test.manifest)\n"
    if "Hilt" in libs:
        dep += "    androidTestImplementation(libs.hilt.android)\n"
        dep += "    kspAndroidTest(libs.hilt.compiler)\n"
    dep += "}\n"



    return pl + an + dep


def settings_gradle(app_name: str) -> str:
    """Génère settings.gradle.kts."""
    return f"""\
pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}
dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}

rootProject.name = "{app_name}"
include(":app")
"""
