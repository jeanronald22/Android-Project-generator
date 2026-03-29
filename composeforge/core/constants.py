"""
composeforge.core.constants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Business constants: available libraries, architectures, and SDK targets.
"""

# Bibliothèques disponibles (labels d'affichage)
LIBRARIES = [
    "Hilt (injection de dépendances)",
    "Retrofit + OkHttp (réseau)",
    "Navigation Compose",
    "Coil (images)",
    "Coroutines + Flow",
    "DataStore Preferences",
    "Room (base de données locale)",
    "Ktor (alternative réseau à Retrofit)",
]

# Clés internes correspondantes (même index que LIBRARIES)
LIB_KEYS = [
    "Hilt",
    "Retrofit",
    "Navigation",
    "Coil",
    "Coroutines",
    "DataStore",
    "Room",
    "Ktor",
]

# Architectures supportées
ARCHS = [
    "Layered (data / domain / presentation)",
    "Feature-based (core + features/...)",
    "Hybride (features/feature/{data,domain,presentation})",
]

# Cibles SDK minimum
MIN_SDKS = [
    ("24", "Android 7.0  — 94% des appareils"),
    ("26", "Android 8.0  — 93% des appareils"),
    ("28", "Android 9.0  — 90% des appareils"),
    ("30", "Android 11   — 82% des appareils"),
]
