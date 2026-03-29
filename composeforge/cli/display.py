"""
composeforge.cli.display
~~~~~~~~~~~~~~~~~~~~~~~~~~
Display functions: header banner, configuration recap, success summary.
"""

from composeforge.cli.colors import C
from composeforge.core.config import ProjectConfig
from composeforge.core.constants import ARCHS


def header() -> None:
    """Affiche la bannière d'accueil."""
    print(f"""
{C.CY}{C.BD}╔══════════════════════════════════════════════════════╗
║       🚀 Android Compose Project Generator           ║
║   Clean Architecture · DI · Libs · Custom Theme      ║
╚══════════════════════════════════════════════════════╝{C.RS}
""")


def print_recap(cfg: ProjectConfig) -> None:
    """Affiche le récapitulatif de la configuration avant génération."""
    libs_text = ", ".join(cfg.libs) if cfg.libs else "Aucune"
    print(f"\n{C.BD}{'─' * 54}{C.RS}")
    print(f"{C.BD}📋 Récapitulatif{C.RS}")
    print(f"  App Name    : {C.CY}{cfg.app_name}{C.RS}")
    print(f"  Package     : {C.CY}{cfg.package}{C.RS}")
    print(f"  Min SDK     : {C.CY}Android {cfg.min_sdk}{C.RS}")
    print(f"  Architecture: {C.CY}{ARCHS[cfg.arch]}{C.RS}")
    print(f"  Librairies  : {C.CY}{libs_text}{C.RS}")
    print(f"{C.BD}{'─' * 54}{C.RS}")


def print_success(cfg: ProjectConfig, output_dir: str) -> None:
    """Affiche le message de succès post-génération."""
    libs_text = ", ".join(cfg.libs) if cfg.libs else "Aucune"
    print(f"""
{C.G}{C.BD}╔══════════════════════════════════════════════════╗
║  ✅  Projet généré avec succès !                 ║
╚══════════════════════════════════════════════════╝{C.RS}

{C.BD}📍 Emplacement :{C.RS}  {output_dir}

{C.BD}📦 Librairies incluses :{C.RS}  {libs_text}

{C.BD}🏗  Architecture :{C.RS}  {ARCHS[cfg.arch]}

{C.BD}🚀 Prochaines étapes :{C.RS}
  1. Ouvrez Android Studio
  2. File → Open → sélectionnez '{output_dir}'
  3. Attendez la synchronisation Gradle (~2 min)
  4. Connectez un appareil ou lancez un émulateur
  5. Run ▶  et profitez !
""")
