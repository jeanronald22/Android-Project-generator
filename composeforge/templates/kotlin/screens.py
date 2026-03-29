"""
composeforge.templates.kotlin.screens
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Screen composable templates.
"""


def kt_home_screen(pkg: str) -> str:
    """Génère HomeScreen.kt."""
    return f"""\
package {pkg}

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp

@Composable
fun HomeScreen(modifier: Modifier = Modifier) {{
    Column(
        modifier            = modifier.fillMaxSize().padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {{
        Text(
            text  = "🚀 Projet prêt !",
            style = MaterialTheme.typography.headlineMedium,
            color = MaterialTheme.colorScheme.primary
        )
        Spacer(Modifier.height(8.dp))
        Text(
            text  = "Clean Architecture · Compose · Hilt",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }}
}}

@Preview(showBackground = true)
@Composable
private fun HomeScreenPreview() {{
    HomeScreen()
}}
"""
