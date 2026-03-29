"""
composeforge.templates.kotlin.database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Room database template.
"""


def kt_room_db(pkg: str, safe_name: str) -> str:
    """Génère la classe Database Room.

    Args:
        pkg: Package de la Database class.
        safe_name: Nom PascalCase pour le nom de la classe.
    """
    return f"""\
package {pkg}

import androidx.room.Database
import androidx.room.RoomDatabase

// Ajoutez vos @Entity classes dans entities = [...]
@Database(
    entities  = [],
    version   = 1,
    exportSchema = false
)
abstract class {safe_name}Database : RoomDatabase() {{
    // Ajoutez vos DAO abstraits ici
    // abstract fun exampleDao(): ExampleDao
}}
"""
