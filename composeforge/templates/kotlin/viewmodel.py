"""
composeforge.templates.kotlin.viewmodel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ViewModel + UiState templates.
"""


def kt_home_viewmodel(pkg: str, core_pkg: str, repo_pkg: str, has_hilt: bool = True) -> str:
    """Génère HomeViewModel.kt avec UiState.

    Args:
        pkg: Package du ViewModel.
        core_pkg: Package des utilitaires core (BaseViewModel).
        repo_pkg: Package de l'interface Repository.
        has_hilt: Si Hilt est sélectionné.
    """
    hilt_imports = ""
    hilt_anno = ""
    inject_anno = ""
    if has_hilt:
        hilt_imports = """import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
"""
        hilt_anno = "@HiltViewModel\n"
        inject_anno = "@Inject "

    return f"""\
package {pkg}

import androidx.lifecycle.viewModelScope
{hilt_imports}import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import {core_pkg}.BaseViewModel
import {repo_pkg}.HomeRepository

/**
 * État UI de l'écran Home.
 */
data class HomeUiState(
    val isLoading: Boolean = false,
    val items: List<String> = emptyList(),
    val error: String? = null
)

/**
 * ViewModel pour l'écran Home.
 */
{hilt_anno}class HomeViewModel {inject_anno}constructor(
    private val repository: HomeRepository
) : BaseViewModel<HomeUiState>(HomeUiState()) {{

    init {{
        loadItems()
    }}

    fun loadItems() {{
        viewModelScope.launch {{
            setState {{ copy(isLoading = true, error = null) }}
            try {{
                repository.getItems().collect {{ items ->
                    setState {{ copy(isLoading = false, items = items) }}
                }}
            }} catch (e: Exception) {{
                setState {{ copy(isLoading = false, error = e.localizedMessage ?: "Erreur inconnue") }}
            }}
        }}
    }}

    fun clearError() {{
        setState {{ copy(error = null) }}
    }}
}}
"""
