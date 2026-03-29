"""
composeforge.templates.kotlin.navigation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Navigation Compose templates: AppNavHost and Screen sealed class.
"""


def kt_nav_host(nav_pkg: str, home_pkg: str) -> str:
    """Génère AppNavHost.kt avec import correct de HomeScreen."""
    return f"""\
package {nav_pkg}

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import {home_pkg}.HomeScreen

@Composable
fun AppNavHost(
    navController: NavHostController,
) {{
    NavHost(
        navController    = navController,
        startDestination = Screen.Home.route
    ) {{
        composable(Screen.Home.route) {{
            HomeScreen()
        }}
    }}
}}
"""


def kt_screen_sealed_class(pkg: str) -> str:
    """Génère Screen.kt (sealed class de routes)."""
    return f"""\
package {pkg}

sealed class Screen(val route: String) {{
    object Home : Screen("home")
}}
"""
