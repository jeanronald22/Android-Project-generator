"""
composeforge.templates.kotlin.repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Repository pattern templates (interface + implementation).
"""


def kt_home_repository(pkg: str) -> str:
    """Génère HomeRepository.kt (interface).

    Args:
        pkg: Package du Repository.
    """
    return f"""\
package {pkg}

import kotlinx.coroutines.flow.Flow

/**
 * Contrat pour l'accès aux données de l'écran Home.
 */
interface HomeRepository {{
    fun getItems(): Flow<List<String>>
}}
"""


def kt_home_repository_impl(pkg: str, repo_iface_pkg: str, has_retrofit: bool = False, api_pkg: str = "") -> str:
    """Génère HomeRepositoryImpl.kt.

    Args:
        pkg: Package de l'implémentation du Repository.
        repo_iface_pkg: Package de l'interface HomeRepository.
        has_retrofit: Si Retrofit est sélectionné.
        api_pkg: Package de l'ApiService (quand Retrofit est activé).
    """
    if has_retrofit:
        return f"""\
package {pkg}

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import {api_pkg}.ApiService
import {repo_iface_pkg}.HomeRepository
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class HomeRepositoryImpl @Inject constructor(
    private val apiService: ApiService
) : HomeRepository {{

    override fun getItems(): Flow<List<String>> = flow {{
        // TODO: Remplacer par un vrai appel réseau
        // val response = apiService.getExampleItems()
        // emit(response.map {{ it.name }})
        emit(listOf("Item 1 (API)", "Item 2 (API)", "Item 3 (API)"))
    }}
}}
"""
    else:
        return f"""\
package {pkg}

import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import {repo_iface_pkg}.HomeRepository
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class HomeRepositoryImpl @Inject constructor() : HomeRepository {{

    override fun getItems(): Flow<List<String>> = flow {{
        // TODO: Remplacer par une vraie source de données
        delay(500) // Simule un temps de chargement
        emit(listOf("Item 1", "Item 2", "Item 3"))
    }}
}}
"""
