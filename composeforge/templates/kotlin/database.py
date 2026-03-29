"""
composeforge.templates.kotlin.database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Room database template.
"""


def kt_room_db(pkg: str, app_name: str) -> str:
    """Génère la classe Database Room."""
    safe = app_name.replace(" ", "")
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
abstract class {safe}Database : RoomDatabase() {{
    // Ajoutez vos DAO abstraits ici
    // abstract fun exampleDao(): ExampleDao
}}
"""
