"""
composeforge.generator.engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Project generator — orchestrates structure creation and file generation.
"""

import os

from composeforge.cli.colors import ok
from composeforge.cli.display import print_success
from composeforge.core.config import ProjectConfig
from composeforge.core.writer import make_dirs, write_file
from composeforge.generator.structure import ArchitectureResolver
from composeforge.templates.gradle import (
    app_gradle,
    root_gradle,
    settings_gradle,
    version_catalog,
)
from composeforge.templates.manifest import manifest
from composeforge.templates.kotlin.activity import kt_application, kt_main_activity
from composeforge.templates.kotlin.core import (
    kt_base_usecase,
    kt_base_viewmodel,
    kt_extensions,
    kt_resource,
)
from composeforge.templates.kotlin.database import kt_room_db
from composeforge.templates.kotlin.di import (
    kt_app_module,
    kt_datastore_module,
    kt_network_module,
    kt_room_module,
)
from composeforge.templates.kotlin.navigation import kt_nav_host, kt_screen_sealed_class
from composeforge.templates.kotlin.screens import kt_home_screen
from composeforge.templates.kotlin.theme import kt_color, kt_theme, kt_type
from composeforge.templates.misc import (
    generate_readme,
    gitignore,
    gradle_properties,
    gradle_wrapper_properties,
    proguard,
)


class ProjectGenerator:
    """Orchestre la génération complète d'un projet Android."""

    def __init__(self, cfg: ProjectConfig, output_dir: str | None = None):
        self.cfg = cfg
        self.output_dir = output_dir or os.path.join(os.getcwd(), cfg.safe_name)

    def generate(self) -> str:
        """Génère le projet complet. Retourne le chemin du dossier créé."""
        from composeforge.cli.colors import C

        print(f"\n{C.BD}{C.CY}⚙  Génération du projet...{C.RS}\n")

        paths = ArchitectureResolver.resolve(self.cfg, self.output_dir)

        self._create_directories(paths)
        self._write_gradle_files()
        self._write_manifest()
        self._write_application()
        self._write_main_activity()
        self._write_theme(paths)
        self._write_home_screen(paths)
        self._write_navigation(paths)
        self._write_di_modules(paths)
        self._write_room_database(paths)
        self._write_core_utilities(paths)
        self._write_misc_files()

        print_success(self.cfg, self.output_dir)
        return self.output_dir

    # ── Private generation steps ─────────────────────

    def _create_directories(self, paths) -> None:
        """Crée l'arborescence de dossiers."""
        common_dirs = [
            os.path.join(self.output_dir, "gradle"),
            os.path.join(self.output_dir, "app", "src", "main", "res"),
        ]
        make_dirs(common_dirs + paths.dirs)
        ok("Structure de dossiers créée")

    def _write_gradle_files(self) -> None:
        """Écrit les fichiers Gradle."""
        base = self.output_dir
        write_file(f"{base}/gradle/libs.versions.toml", version_catalog(self.cfg.libs))
        write_file(f"{base}/build.gradle.kts", root_gradle())
        write_file(f"{base}/app/build.gradle.kts", app_gradle(self.cfg))
        write_file(f"{base}/settings.gradle.kts", settings_gradle(self.cfg.app_name))
        write_file(f"{base}/gradle.properties", gradle_properties())
        ok("Fichiers Gradle configurés")

    def _write_manifest(self) -> None:
        """Écrit AndroidManifest.xml."""
        write_file(
            f"{self.output_dir}/app/src/main/AndroidManifest.xml",
            manifest(self.cfg),
        )
        ok("AndroidManifest.xml généré")

    def _write_application(self) -> None:
        """Écrit MyApplication.kt si Hilt est sélectionné."""
        if self.cfg.has_lib("Hilt"):
            from composeforge.core.writer import pkg_to_path

            pp = pkg_to_path(self.output_dir, self.cfg.package)
            write_file(f"{pp}/MyApplication.kt", kt_application(self.cfg.package))
            ok("MyApplication.kt généré")

    def _write_main_activity(self) -> None:
        """Écrit MainActivity.kt."""
        from composeforge.core.writer import pkg_to_path

        pp = pkg_to_path(self.output_dir, self.cfg.package)
        write_file(f"{pp}/MainActivity.kt", kt_main_activity(self.cfg))
        ok("MainActivity.kt généré")

    def _write_theme(self, paths) -> None:
        """Écrit les fichiers de thème Material 3."""
        write_file(f"{paths.theme_dir}/Color.kt", kt_color(paths.theme_pkg))
        write_file(f"{paths.theme_dir}/Type.kt", kt_type(paths.theme_pkg))
        write_file(f"{paths.theme_dir}/Theme.kt", kt_theme(paths.theme_pkg, self.cfg.app_name))
        ok("Thème Material 3 généré (Color, Type, Theme)")

    def _write_home_screen(self, paths) -> None:
        """Écrit HomeScreen.kt."""
        write_file(f"{paths.home_dir}/HomeScreen.kt", kt_home_screen(paths.home_pkg))
        ok("HomeScreen.kt généré")

    def _write_navigation(self, paths) -> None:
        """Écrit les fichiers de navigation si Navigation est sélectionnée."""
        if self.cfg.has_lib("Navigation"):
            write_file(f"{paths.nav_dir}/AppNavHost.kt", kt_nav_host(paths.nav_pkg))
            write_file(f"{paths.nav_dir}/Screen.kt", kt_screen_sealed_class(paths.nav_pkg))
            ok("Navigation Compose configurée")

    def _write_di_modules(self, paths) -> None:
        """Écrit les modules Hilt DI."""
        if self.cfg.has_lib("Hilt"):
            write_file(f"{paths.di_dir}/AppModule.kt", kt_app_module(paths.di_pkg))
            if self.cfg.has_lib("Retrofit"):
                write_file(f"{paths.di_dir}/NetworkModule.kt", kt_network_module(paths.di_pkg))
            if self.cfg.has_lib("DataStore"):
                write_file(f"{paths.di_dir}/DataStoreModule.kt", kt_datastore_module(paths.di_pkg))
            if self.cfg.has_lib("Room"):
                write_file(
                    f"{paths.di_dir}/DatabaseModule.kt",
                    kt_room_module(paths.di_pkg, self.cfg.app_name),
                )
            ok("Modules Hilt générés")

    def _write_room_database(self, paths) -> None:
        """Écrit la classe Room Database."""
        if self.cfg.has_lib("Room"):
            if self.cfg.arch == 0:
                from composeforge.core.writer import pkg_to_path

                pp = pkg_to_path(self.output_dir, self.cfg.package)
                db_dir = f"{pp}/data/local"
                db_pkg = f"{self.cfg.package}.data.local"
            else:
                from composeforge.core.writer import pkg_to_path

                pp = pkg_to_path(self.output_dir, self.cfg.package)
                db_dir = f"{pp}/features/home/data/local"
                db_pkg = f"{self.cfg.package}.features.home.data.local"
            write_file(
                f"{db_dir}/{self.cfg.safe_name}Database.kt",
                kt_room_db(db_pkg, self.cfg.app_name),
            )
            ok("Room Database généré")

    def _write_core_utilities(self, paths) -> None:
        """Écrit les utilitaires core."""
        write_file(f"{paths.core_dir}/Resource.kt", kt_resource(paths.core_pkg))
        write_file(f"{paths.core_dir}/Extensions.kt", kt_extensions(paths.core_pkg))
        write_file(f"{paths.core_dir}/BaseUseCase.kt", kt_base_usecase(paths.core_pkg))
        write_file(f"{paths.core_dir}/BaseViewModel.kt", kt_base_viewmodel(paths.core_pkg))
        ok("Utilitaires core générés (Resource, BaseUseCase, Extensions, BaseViewModel)")

    def _write_misc_files(self) -> None:
        """Écrit les fichiers divers (README, gitignore, proguard, wrapper)."""
        base = self.output_dir
        write_file(f"{base}/app/proguard-rules.pro", proguard())
        ok("proguard-rules.pro généré")

        write_file(f"{base}/.gitignore", gitignore())
        ok(".gitignore généré")

        write_file(
            f"{base}/gradle/wrapper/gradle-wrapper.properties",
            gradle_wrapper_properties(),
        )
        ok("Gradle Wrapper configuré")

        write_file(f"{base}/README.md", generate_readme(self.cfg))
        ok("README.md généré")
