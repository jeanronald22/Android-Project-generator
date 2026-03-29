"""
composeforge.core.config
~~~~~~~~~~~~~~~~~~~~~~~~~
Typed project configuration — replaces the raw dict with a dataclass.
"""

import re
from dataclasses import dataclass, field
from typing import List


def _to_pascal_case(name: str) -> str:
    """Convertit un nom arbitraire en PascalCase valide pour Kotlin.

    Exemples:
        'My-Cool-App'  -> 'MyCoolApp'
        'mon app 2'    -> 'MonApp2'
        'test_app'     -> 'TestApp'
        '  hello  '    -> 'Hello'
        '123app'       -> 'App123App'
    """
    # Sépare sur tout caractère non-alphanumérique
    words = re.split(r"[^a-zA-Z0-9]+", name.strip())
    # Capitalise chaque mot, filtre les vides
    result = []
    for w in words:
        if not w:
            continue
        # Sépare aussi les transitions chiffre→lettre pour capitaliser
        parts = re.split(r"(?<=\d)(?=[a-zA-Z])", w)
        result.extend(p[0].upper() + p[1:] if p[0].isalpha() else p for p in parts)
    pascal = "".join(result)
    # Si commence par un chiffre, préfixer avec 'App'
    if pascal and pascal[0].isdigit():
        pascal = "App" + pascal
    return pascal or "MyApp"


@dataclass
class ProjectConfig:
    """Configuration complète d'un projet Android à générer."""

    app_name: str
    package: str
    min_sdk: str
    arch: int               # 0 = Layered, 1 = Feature-based, 2 = Hybrid
    libs: List[str] = field(default_factory=list)

    # ── Derived properties ───────────────────────────

    @property
    def safe_name(self) -> str:
        """Nom PascalCase valide pour classes Kotlin et dossiers.

        'My-Cool-App' -> 'MyCoolApp'
        """
        return _to_pascal_case(self.app_name)

    @property
    def db_name(self) -> str:
        """Nom lowercase pour le fichier .db Room."""
        return self.safe_name.lower()

    def has_lib(self, key: str) -> bool:
        """Vérifie si une bibliothèque est sélectionnée."""
        return key in self.libs

    def has_any_lib(self, *keys: str) -> bool:
        """Vérifie si au moins une des bibliothèques est sélectionnée."""
        return any(k in self.libs for k in keys)
