"""
composeforge.templates.kotlin.screens
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Screen composable templates.
"""


def kt_home_screen(pkg: str, vm_pkg: str = "", has_hilt: bool = True) -> str:
    """Génère HomeScreen.kt connecté au ViewModel.

    Args:
        pkg: Package du Screen.
        vm_pkg: Package du ViewModel.
        has_hilt: Si Hilt est sélectionné (pour hiltViewModel()).
    """
    if vm_pkg and has_hilt:
        return f"""\
package {pkg}

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import {vm_pkg}.HomeViewModel

@Composable
fun HomeScreen(
    modifier: Modifier = Modifier,
    viewModel: HomeViewModel = hiltViewModel()
) {{
    val uiState by viewModel.state.collectAsStateWithLifecycle()

    Box(
        modifier = modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {{
        when {{
            uiState.isLoading -> {{
                CircularProgressIndicator()
            }}
            uiState.error != null -> {{
                Column(horizontalAlignment = Alignment.CenterHorizontally) {{
                    Text(
                        text  = uiState.error ?: "Erreur",
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.error
                    )
                }}
            }}
            else -> {{
                LazyColumn(
                    modifier            = Modifier.fillMaxSize().padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {{
                    items(uiState.items) {{ item ->
                        Card(
                            colors    = CardDefaults.cardColors(
                                containerColor = MaterialTheme.colorScheme.surfaceVariant
                            ),
                            modifier  = Modifier.fillParentMaxWidth()
                        ) {{
                            Text(
                                text     = item,
                                style    = MaterialTheme.typography.bodyLarge,
                                modifier = Modifier.padding(16.dp)
                            )
                        }}
                    }}
                }}
            }}
        }}
    }}
}}
"""
    # Fallback : pas de ViewModel (pas de Hilt)
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
            text  = "Clean Architecture · Compose",
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
