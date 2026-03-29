"""
composeforge.templates.kotlin.navigation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Navigation Compose templates: AppNavHost and Screen sealed class.
"""


def kt_nav_host(pkg: str) -> str:
    """Génère AppNavHost.kt."""
    return f"""\
package {pkg}

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable

@Composable
fun AppNavHost(
    navController: NavHostController,
) {{
    NavHost(
        navController    = navController,
        startDestination = Screen.Home.route
    ) {{
        composable(Screen.Home.route) {{
            // HomeScreen sera importé depuis le package features/presentation
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
