"""
composeforge.core.writer
~~~~~~~~~~~~~~~~~~~~~~~~~
File-system helpers: directory creation and file writing.
"""

import os
from typing import List


def make_dirs(path_list: List[str]) -> None:
    """Crée une liste de répertoires (récursif, idempotent)."""
    for p in path_list:
        os.makedirs(p, exist_ok=True)


def write_file(path: str, content: str) -> None:
    """Écrit du contenu dans un fichier, crée les répertoires parents si besoin."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def pkg_to_path(base_dir: str, package: str) -> str:
    """Convertit un base_dir + package name en chemin Java source.

    Ex: pkg_to_path('/out/MyApp', 'com.example.app')
        -> '/out/MyApp/app/src/main/java/com/example/app'
    """
    return os.path.join(base_dir, "app", "src", "main", "java", *package.split("."))
