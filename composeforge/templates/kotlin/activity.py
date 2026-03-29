"""
composeforge.templates.kotlin.activity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MainActivity and Application class templates.
"""

from composeforge.core.config import ProjectConfig


def kt_application(pkg: str) -> str:
    """Génère MyApplication.kt (Hilt @HiltAndroidApp)."""
    return f"""\
package {pkg}

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class MyApplication : Application()
"""


def kt_main_activity(cfg: ProjectConfig) -> str:
    """Génère MainActivity.kt."""
    pkg = cfg.package
    libs = cfg.libs
    arch = cfg.arch

    hilt_import = "import dagger.hilt.android.AndroidEntryPoint\n" if "Hilt" in libs else ""
    hilt_anno = "@AndroidEntryPoint\n" if "Hilt" in libs else ""
    nav_import = "import androidx.navigation.compose.rememberNavController\n" if "Navigation" in libs else ""

    # Resolve package paths depending on architecture
    if arch == 0:
        theme_pkg = f"{pkg}.presentation.theme"
        home_pkg = f"{pkg}.presentation.screens.home"
        nav_pkg = f"{pkg}.presentation.navigation"
    else:
        theme_pkg = f"{pkg}.core.theme"
        home_pkg = f"{pkg}.features.home.presentation.screens"
        nav_pkg = f"{pkg}.core.navigation"

    # Imports conditionnels
    if "Navigation" in libs:
        content = "AppNavHost(navController = rememberNavController())"
        screen_imports = f"import {nav_pkg}.AppNavHost"
    else:
        content = "HomeScreen()"
        screen_imports = f"import {home_pkg}.HomeScreen"

    return f"""\
package {pkg}

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
{hilt_import}{nav_import}import {theme_pkg}.AppTheme
{screen_imports}

{hilt_anno}class MainActivity : ComponentActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {{
            AppTheme {{
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {{
                    {content}
                }}
            }}
        }}
    }}
}}
"""

