"""
composeforge.__main__
~~~~~~~~~~~~~~~~~~~~~~
CLI entry point — ``python -m composeforge``.
"""

import sys

from composeforge.cli.colors import err, warn
from composeforge.cli.display import header, print_recap
from composeforge.cli.prompts import ask, ask_choice, ask_multi
from composeforge.core.config import ProjectConfig
from composeforge.core.constants import ARCHS, LIB_KEYS, LIBRARIES, MIN_SDKS
from composeforge.generator.engine import ProjectGenerator


def main() -> None:
    """Point d'entrée principal du CLI."""
    dry_run = "--dry-run" in sys.argv

    header()

    # ── 1. Collect inputs ────────────────────────────
    app_name = ask("Nom de l'application", "MyApp")
    if not app_name:
        err("Le nom ne peut pas être vide.")
        sys.exit(1)

    default_pkg = f"com.example.{app_name.lower().replace(' ', '').replace('-', '')}"
    package = ask("Package name", default_pkg)
    if not package or "." not in package:
        warn("Package invalide, utilisation du package par défaut.")
        package = default_pkg

    sdk_labels = [f"{s[0]}  — {s[1]}" for s in MIN_SDKS]
    sdk_idx = ask_choice("SDK minimum cible", sdk_labels)
    min_sdk = MIN_SDKS[sdk_idx][0]

    arch = ask_choice("Architecture Clean", ARCHS)

    lib_idx = ask_multi("Bibliothèques à inclure (sélection multiple)", LIBRARIES)
    libs = [LIB_KEYS[i] for i in lib_idx]

    # ── 2. Build config ──────────────────────────────
    cfg = ProjectConfig(
        app_name=app_name,
        package=package,
        min_sdk=min_sdk,
        arch=arch,
        libs=libs,
    )

    # ── 3. Confirm ───────────────────────────────────
    print_recap(cfg)

    generator = ProjectGenerator(cfg)

    # ── 4. Dry-run / Preview ─────────────────────────
    if dry_run:
        generator.preview()
        sys.exit(0)

    confirm = ask("Voir l'arborescence (p), Générer (o), ou Annuler (n) ?", "o")
    if confirm and confirm.lower() in ("p", "preview", "dry-run"):
        generator.preview()
        confirm = ask("Générer le projet ? (o/n)", "o")

    if confirm and confirm.lower() not in ("o", "oui", "y", "yes"):
        from composeforge.cli.colors import C

        print(f"\n{C.Y}Annulé.{C.RS}")
        sys.exit(0)

    # ── 5. Generate ──────────────────────────────────
    generator.generate()


if __name__ == "__main__":
    main()
