"""
composeforge.templates.kotlin.di
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Hilt dependency injection module templates.
"""


def kt_app_module(pkg: str) -> str:
    """Génère AppModule.kt (Hilt)."""
    return f"""\
package {pkg}

import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent

@Module
@InstallIn(SingletonComponent::class)
object AppModule {{
    // Liez ici vos dépendances de niveau application
}}
"""


def kt_network_module(pkg: str) -> str:
    """Génère NetworkModule.kt (Hilt + Retrofit + OkHttp)."""
    return f"""\
package {pkg}

import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {{

    private const val BASE_URL     = "https://api.example.com/"
    private const val TIMEOUT_SEC  = 30L

    @Provides @Singleton
    fun provideOkHttpClient(): OkHttpClient =
        OkHttpClient.Builder()
            .addInterceptor(
                HttpLoggingInterceptor().apply {{
                    level = HttpLoggingInterceptor.Level.BODY
                }}
            )
            .connectTimeout(TIMEOUT_SEC, TimeUnit.SECONDS)
            .readTimeout(TIMEOUT_SEC, TimeUnit.SECONDS)
            .build()

    @Provides @Singleton
    fun provideRetrofit(client: OkHttpClient): Retrofit =
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
}}
"""


def kt_datastore_module(pkg: str) -> str:
    """Génère DataStoreModule.kt (Hilt + DataStore)."""
    return f"""\
package {pkg}

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.preferencesDataStore
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "app_prefs")

@Module
@InstallIn(SingletonComponent::class)
object DataStoreModule {{

    @Provides @Singleton
    fun provideDataStore(@ApplicationContext ctx: Context): DataStore<Preferences> =
        ctx.dataStore
}}
"""


def kt_room_module(di_pkg: str, db_pkg: str, safe_name: str, db_name: str) -> str:
    """Génère DatabaseModule.kt (Hilt + Room).

    Args:
        di_pkg: Package du module DI (ex: com.example.app.di)
        db_pkg: Package où se trouve la Database class (ex: com.example.app.data.local)
        safe_name: Nom PascalCase de l'app (ex: MyCoolApp)
        db_name: Nom lowercase pour le fichier .db (ex: mycoolapp)
    """
    return f"""\
package {di_pkg}

import android.content.Context
import androidx.room.Room
import {db_pkg}.{safe_name}Database
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {{

    @Provides @Singleton
    fun provide{safe_name}Database(@ApplicationContext ctx: Context): {safe_name}Database =
        Room.databaseBuilder(
            ctx,
            {safe_name}Database::class.java,
            "{db_name}.db"
        ).build()
}}
"""
