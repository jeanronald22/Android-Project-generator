"""
composeforge.templates.kotlin.database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Room database / entity / DAO templates.
"""


def kt_room_db(pkg: str, safe_name: str) -> str:
    """Génère la classe Database Room avec une entité par défaut.

    Args:
        pkg: Package de la Database class.
        safe_name: Nom PascalCase pour le nom de la classe.
    """
    return f"""\
package {pkg}

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(
    entities  = [AppEntity::class],
    version   = 1,
    exportSchema = false
)
abstract class {safe_name}Database : RoomDatabase() {{
    abstract fun appDao(): AppDao
}}
"""


def kt_room_entity(pkg: str) -> str:
    """Génère une @Entity Room par défaut (AppEntity).

    Args:
        pkg: Package de la classe Entity.
    """
    return f"""\
package {pkg}

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "app_items")
data class AppEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val name: String = "",
    val createdAt: Long = System.currentTimeMillis()
)
"""


def kt_room_dao(pkg: str) -> str:
    """Génère un @Dao Room par défaut (AppDao).

    Args:
        pkg: Package de la classe DAO.
    """
    return f"""\
package {pkg}

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

@Dao
interface AppDao {{

    @Query("SELECT * FROM app_items ORDER BY createdAt DESC")
    fun getAll(): Flow<List<AppEntity>>

    @Query("SELECT * FROM app_items WHERE id = :id")
    suspend fun getById(id: Long): AppEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(entity: AppEntity): Long

    @Update
    suspend fun update(entity: AppEntity)

    @Delete
    suspend fun delete(entity: AppEntity)
}}
"""
