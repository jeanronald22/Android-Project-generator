"""
composeforge.core.config
~~~~~~~~~~~~~~~~~~~~~~~~~
Typed project configuration — replaces the raw dict with a dataclass.
"""

from dataclasses import dataclass, field
from typing import List


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
        """Nom sans espaces, utilisable pour les noms de classes/dossiers."""
        return self.app_name.replace(" ", "")

    def has_lib(self, key: str) -> bool:
        """Vérifie si une bibliothèque est sélectionnée."""
        return key in self.libs

    def has_any_lib(self, *keys: str) -> bool:
        """Vérifie si au moins une des bibliothèques est sélectionnée."""
        return any(k in self.libs for k in keys)
