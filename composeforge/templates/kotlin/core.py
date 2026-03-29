"""
composeforge.templates.kotlin.core
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Core utility templates: Resource, BaseUseCase, Extensions, BaseViewModel.
"""


def kt_resource(pkg: str) -> str:
    """Génère Resource.kt (sealed class wrapper)."""
    return f"""\
package {pkg}

/**
 * Wrapper générique pour gérer les états asynchrones.
 * Usage : Flow<Resource<T>> dans vos UseCases et ViewModels.
 */
sealed class Resource<out T> {{
    data class  Success<T>(val data: T)                                       : Resource<T>()
    data class  Error(val message: String, val cause: Throwable? = null)      : Resource<Nothing>()
    object      Loading                                                        : Resource<Nothing>()

    val isSuccess get() = this is Success
    val isError   get() = this is Error
    val isLoading get() = this is Loading
}}
"""


def kt_base_usecase(pkg: str) -> str:
    """Génère BaseUseCase.kt."""
    return f"""\
package {pkg}

import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * UseCase de base — wrap l'exécution dans un dispatcher IO par défaut.
 */
abstract class BaseUseCase<in P, out R>(
    private val dispatcher: CoroutineDispatcher = Dispatchers.IO
) {{
    suspend operator fun invoke(params: P): R = withContext(dispatcher) {{ execute(params) }}
    protected abstract suspend fun execute(params: P): R
}}

/** Sentinel pour les UseCases sans paramètre. */
object NoParams
"""


def kt_extensions(pkg: str) -> str:
    """Génère Extensions.kt (Flow → Resource)."""
    return f"""\
package {pkg}

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onStart

/** Transforme un Flow<T> en Flow<Resource<T>>. */
fun <T> Flow<T>.asResource(): Flow<Resource<T>> =
    this
        .map<T, Resource<T>> {{ Resource.Success(it) }}
        .onStart {{ emit(Resource.Loading) }}
        .catch   {{ e -> emit(Resource.Error(e.localizedMessage ?: "Erreur inconnue", e)) }}
"""


def kt_base_viewmodel(pkg: str) -> str:
    """Génère BaseViewModel.kt."""
    return f"""\
package {pkg}

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

/**
 * ViewModel de base avec gestion d'état via StateFlow.
 * Héritez de cette classe et définissez votre UiState.
 */
abstract class BaseViewModel<S>(initialState: S) : ViewModel() {{
    private val _state = MutableStateFlow(initialState)
    val state: StateFlow<S> = _state.asStateFlow()

    protected fun setState(reducer: S.() -> S) {{
        _state.value = _state.value.reducer()
    }}
}}
"""
