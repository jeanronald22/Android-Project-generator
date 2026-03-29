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
        nav_pkg = f"{pkg}.presentation.navigation"
    else:
        theme_pkg = f"{pkg}.core.theme"
        nav_pkg = f"{pkg}.core.navigation"

    content = "AppNavHost(navController = rememberNavController())" if "Navigation" in libs else "HomeScreen()"

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
{f"import {nav_pkg}.AppNavHost" if "Navigation" in libs else ""}

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
