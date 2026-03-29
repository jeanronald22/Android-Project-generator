"""
composeforge.templates.manifest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
AndroidManifest.xml template.
"""

from composeforge.core.config import ProjectConfig


def manifest(cfg: ProjectConfig) -> str:
    """Génère AndroidManifest.xml."""
    name = cfg.app_name
    safe = cfg.safe_name
    app_attr = '\n        android:name=".MyApplication"' if cfg.has_lib("Hilt") else ""
    net = '    <uses-permission android:name="android.permission.INTERNET" />\n' if cfg.has_any_lib("Retrofit", "Ktor") else ""

    return f"""\
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

{net}\
    <application{app_attr}
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="{name}"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{safe}">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
"""
