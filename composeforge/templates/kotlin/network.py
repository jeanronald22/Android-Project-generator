"""
composeforge.templates.kotlin.network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Retrofit ApiService template.
"""


def kt_api_service(pkg: str) -> str:
    """Génère ApiService.kt (interface Retrofit).

    Args:
        pkg: Package de l'ApiService.
    """
    return f"""\
package {pkg}

import retrofit2.http.GET

/**
 * Interface Retrofit pour les appels réseau.
 * Ajoutez vos endpoints ici.
 */
interface ApiService {{

    @GET("items")
    suspend fun getExampleItems(): List<ExampleItemDto>
}}

/**
 * DTO exemple pour les réponses API.
 * Remplacez par vos propres modèles.
 */
data class ExampleItemDto(
    val id: Int,
    val name: String,
    val description: String? = null
)
"""
