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
from composeforge.templates.kotlin.database import kt_room_db, kt_room_entity, kt_room_dao
from composeforge.templates.kotlin.tests import kt_example_unit_test, kt_example_instrumented_test
from composeforge.templates.kotlin.viewmodel import kt_home_viewmodel
from composeforge.templates.kotlin.repository import kt_home_repository, kt_home_repository_impl
from composeforge.templates.kotlin.network import kt_api_service
from composeforge.templates.kotlin.di import (
    kt_app_module,
    kt_datastore_module,
    kt_network_module,
    kt_room_module,
    kt_repository_module,
)
from composeforge.templates.kotlin.navigation import kt_nav_host, kt_screen_sealed_class
from composeforge.templates.kotlin.screens import kt_home_screen
from composeforge.templates.kotlin.theme import kt_color, kt_theme, kt_type
from composeforge.templates.misc import (
    generate_readme,
    github_actions_ci,
    gitignore,
    gradle_properties,
    gradle_wrapper_properties,
    proguard,
)
from composeforge.templates.resources import (
    backup_rules_xml,
    ic_launcher_background_xml,
    ic_launcher_foreground_xml,
    ic_launcher_round_xml,
    ic_launcher_xml,
    strings_xml,
    themes_night_xml,
    themes_xml,
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
        self._write_resources()
        self._write_application()
        self._write_main_activity()
        self._write_theme(paths)
        self._write_home_screen(paths)
        self._write_home_viewmodel(paths)
        self._write_repositories(paths)
        self._write_api_service(paths)
        self._write_navigation(paths)
        self._write_di_modules(paths)
        self._write_room_database(paths)
        self._write_core_utilities(paths)
        self._write_test_files()
        self._write_misc_files()

        print_success(self.cfg, self.output_dir)
        return self.output_dir

    def preview(self) -> None:
        """Affiche l'arborescence des fichiers qui seraient générés (dry-run)."""
        from composeforge.cli.colors import C
        from composeforge.core.writer import pkg_to_path

        paths = ArchitectureResolver.resolve(self.cfg, self.output_dir)
        pp = pkg_to_path(self.output_dir, self.cfg.package)
        files = []

        # ── Gradle ──
        files += [
            "gradle/libs.versions.toml",
            "gradle/wrapper/gradle-wrapper.properties",
            "build.gradle.kts",
            "app/build.gradle.kts",
            "settings.gradle.kts",
            "gradle.properties",
        ]

        # ── Manifest ──
        files.append("app/src/main/AndroidManifest.xml")

        # ── Resources ──
        files += [
            "app/src/main/res/values/strings.xml",
            "app/src/main/res/values/themes.xml",
            "app/src/main/res/values/ic_launcher_background.xml",
            "app/src/main/res/values-night/themes.xml",
            "app/src/main/res/drawable-v24/ic_launcher_foreground.xml",
            "app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml",
            "app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml",
            "app/src/main/res/xml/backup_rules.xml",
        ]

        # ── Kotlin source path prefix ──
        src = f"app/src/main/java/{self.cfg.package.replace('.', '/')}"

        # ── App class ──
        if self.cfg.has_lib("Hilt"):
            files.append(f"{src}/MyApplication.kt")
        files.append(f"{src}/MainActivity.kt")

        # ── Theme ──
        theme = os.path.relpath(paths.theme_dir, self.output_dir)
        files += [f"{theme}/Color.kt", f"{theme}/Type.kt", f"{theme}/Theme.kt"]

        # ── Screens ──
        home = os.path.relpath(paths.home_dir, self.output_dir)
        files.append(f"{home}/HomeScreen.kt")

        # ── ViewModel ──
        if self.cfg.has_lib("Hilt"):
            vm = os.path.relpath(paths.vm_dir, self.output_dir)
            files.append(f"{vm}/HomeViewModel.kt")

        # ── Repository ──
        ri = os.path.relpath(paths.repo_iface_dir, self.output_dir)
        files.append(f"{ri}/HomeRepository.kt")
        rim = os.path.relpath(paths.repo_impl_dir, self.output_dir)
        files.append(f"{rim}/HomeRepositoryImpl.kt")

        # ── ApiService ──
        if self.cfg.has_lib("Retrofit"):
            api = os.path.relpath(paths.api_dir, self.output_dir)
            files.append(f"{api}/ApiService.kt")

        # ── Navigation ──
        if self.cfg.has_lib("Navigation"):
            nav = os.path.relpath(paths.nav_dir, self.output_dir)
            files += [f"{nav}/AppNavHost.kt", f"{nav}/Screen.kt"]

        # ── DI ──
        if self.cfg.has_lib("Hilt"):
            di = os.path.relpath(paths.di_dir, self.output_dir)
            files.append(f"{di}/AppModule.kt")
            if self.cfg.has_lib("Retrofit"):
                files.append(f"{di}/NetworkModule.kt")
            if self.cfg.has_lib("DataStore"):
                files.append(f"{di}/DataStoreModule.kt")
            if self.cfg.has_lib("Room"):
                files.append(f"{di}/DatabaseModule.kt")
            files.append(f"{di}/RepositoryModule.kt")

        # ── Room ──
        if self.cfg.has_lib("Room"):
            if self.cfg.arch == 0:
                db = f"{src}/data/local"
            else:
                db = f"{src}/features/home/data/local"
            files += [
                f"{db}/{self.cfg.safe_name}Database.kt",
                f"{db}/AppEntity.kt",
                f"{db}/AppDao.kt",
            ]

        # ── Core ──
        core = os.path.relpath(paths.core_dir, self.output_dir)
        files += [
            f"{core}/Resource.kt",
            f"{core}/Extensions.kt",
            f"{core}/BaseUseCase.kt",
            f"{core}/BaseViewModel.kt",
        ]

        # ── Tests ──
        test_src = f"app/src/test/java/{self.cfg.package.replace('.', '/')}"
        atest_src = f"app/src/androidTest/java/{self.cfg.package.replace('.', '/')}"
        files += [
            f"{test_src}/ExampleUnitTest.kt",
            f"{atest_src}/ExampleInstrumentedTest.kt",
        ]

        # ── Misc ──
        files += ["app/proguard-rules.pro", ".gitignore", "README.md", ".github/workflows/build.yml"]

        # ── Build and print tree ──
        self._print_tree(files)

    def _print_tree(self, files: list) -> None:
        """Affiche une liste de fichiers sous forme d'arborescence colorée."""
        from composeforge.cli.colors import C

        # Build a nested dict from file paths
        tree: dict = {}
        for f in sorted(files):
            parts = f.split("/")
            node = tree
            for part in parts:
                node = node.setdefault(part, {})

        project_name = os.path.basename(self.output_dir)
        print(f"\n{C.BD}{C.CY}📂 {project_name}/{C.RS}")
        self._render_tree(tree, prefix="")

        count_files = len(files)
        # Count unique directories
        dirs = set()
        for f in files:
            parts = f.split("/")
            for i in range(1, len(parts)):
                dirs.add("/".join(parts[:i]))
        print(f"\n{C.BD}  {len(dirs)} répertoires, {count_files} fichiers{C.RS}\n")

    def _render_tree(self, node: dict, prefix: str) -> None:
        """Affiche récursivement l'arborescence avec connecteurs."""
        from composeforge.cli.colors import C

        entries = list(node.items())
        for i, (name, children) in enumerate(entries):
            is_last = (i == len(entries) - 1)
            connector = "└── " if is_last else "├── "
            if children:  # directory
                print(f"{prefix}{connector}{C.CY}{name}/{C.RS}")
                extension = "    " if is_last else "│   "
                self._render_tree(children, prefix + extension)
            else:  # file
                # Color by extension
                if name.endswith(".kt"):
                    color = C.B
                elif name.endswith(".xml"):
                    color = C.Y
                elif name.endswith(".kts") or name.endswith(".toml") or name.endswith(".properties"):
                    color = C.G
                else:
                    color = C.RS
                print(f"{prefix}{connector}{color}{name}{C.RS}")

    # ── Private generation steps ─────────────────────

    def _create_directories(self, paths) -> None:
        """Crée l'arborescence de dossiers."""
        res = os.path.join(self.output_dir, "app", "src", "main", "res")
        common_dirs = [
            os.path.join(self.output_dir, "gradle"),
            res,
            f"{res}/values",
            f"{res}/values-night",
            f"{res}/drawable",
            f"{res}/drawable-v24",
            f"{res}/mipmap-anydpi-v26",
            f"{res}/xml",
            os.path.join(self.output_dir, "app", "src", "test", "java"),
            os.path.join(self.output_dir, "app", "src", "androidTest", "java"),
        ]
        make_dirs(common_dirs + paths.dirs)
        ok("Structure de dossiers créée")

    def _write_gradle_files(self) -> None:
        """Écrit les fichiers Gradle."""
        base = self.output_dir
        write_file(f"{base}/gradle/libs.versions.toml", version_catalog(self.cfg.libs))
        write_file(f"{base}/build.gradle.kts", root_gradle(self.cfg.libs))
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

    def _write_resources(self) -> None:
        """Écrit les fichiers de ressources Android (strings, themes, icons)."""
        res = f"{self.output_dir}/app/src/main/res"
        safe = self.cfg.safe_name

        write_file(f"{res}/values/strings.xml", strings_xml(self.cfg.app_name))
        write_file(f"{res}/values/themes.xml", themes_xml(safe))
        write_file(f"{res}/values/ic_launcher_background.xml", ic_launcher_background_xml())
        write_file(f"{res}/values-night/themes.xml", themes_night_xml(safe))
        write_file(f"{res}/drawable-v24/ic_launcher_foreground.xml", ic_launcher_foreground_xml())
        write_file(f"{res}/mipmap-anydpi-v26/ic_launcher.xml", ic_launcher_xml())
        write_file(f"{res}/mipmap-anydpi-v26/ic_launcher_round.xml", ic_launcher_round_xml())
        write_file(f"{res}/xml/backup_rules.xml", backup_rules_xml())
        ok("Ressources Android générées (strings, themes, icons)")

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
        write_file(f"{paths.theme_dir}/Theme.kt", kt_theme(paths.theme_pkg, self.cfg.safe_name))
        ok("Thème Material 3 généré (Color, Type, Theme)")

    def _write_home_screen(self, paths) -> None:
        """Écrit HomeScreen.kt."""
        has_hilt = self.cfg.has_lib("Hilt")
        vm_pkg = paths.vm_pkg if has_hilt else ""
        write_file(
            f"{paths.home_dir}/HomeScreen.kt",
            kt_home_screen(paths.home_pkg, vm_pkg=vm_pkg, has_hilt=has_hilt),
        )
        ok("HomeScreen.kt généré")

    def _write_home_viewmodel(self, paths) -> None:
        """Écrit HomeViewModel.kt si Hilt est sélectionné."""
        if self.cfg.has_lib("Hilt"):
            write_file(
                f"{paths.vm_dir}/HomeViewModel.kt",
                kt_home_viewmodel(
                    pkg=paths.vm_pkg,
                    core_pkg=paths.core_pkg,
                    repo_pkg=paths.repo_iface_pkg,
                    has_hilt=True,
                ),
            )
            ok("HomeViewModel.kt généré")

    def _write_repositories(self, paths) -> None:
        """Écrit l'interface et l'impl du Repository."""
        write_file(
            f"{paths.repo_iface_dir}/HomeRepository.kt",
            kt_home_repository(paths.repo_iface_pkg),
        )
        has_retrofit = self.cfg.has_lib("Retrofit")
        write_file(
            f"{paths.repo_impl_dir}/HomeRepositoryImpl.kt",
            kt_home_repository_impl(
                pkg=paths.repo_impl_pkg,
                repo_iface_pkg=paths.repo_iface_pkg,
                has_retrofit=has_retrofit,
                api_pkg=paths.api_pkg if has_retrofit else "",
            ),
        )
        ok("Repository (interface + impl) généré")

    def _write_api_service(self, paths) -> None:
        """Écrit ApiService.kt si Retrofit est sélectionné."""
        if self.cfg.has_lib("Retrofit"):
            write_file(
                f"{paths.api_dir}/ApiService.kt",
                kt_api_service(paths.api_pkg),
            )
            ok("ApiService.kt généré")

    def _write_navigation(self, paths) -> None:
        """Écrit les fichiers de navigation si Navigation est sélectionnée."""
        if self.cfg.has_lib("Navigation"):
            write_file(f"{paths.nav_dir}/AppNavHost.kt", kt_nav_host(paths.nav_pkg, paths.home_pkg))
            write_file(f"{paths.nav_dir}/Screen.kt", kt_screen_sealed_class(paths.nav_pkg))
            ok("Navigation Compose configurée")

    def _write_di_modules(self, paths) -> None:
        """Écrit les modules Hilt DI."""
        if self.cfg.has_lib("Hilt"):
            write_file(f"{paths.di_dir}/AppModule.kt", kt_app_module(paths.di_pkg))
            if self.cfg.has_lib("Retrofit"):
                write_file(
                    f"{paths.di_dir}/NetworkModule.kt",
                    kt_network_module(paths.di_pkg, api_pkg=paths.api_pkg),
                )
            if self.cfg.has_lib("DataStore"):
                write_file(f"{paths.di_dir}/DataStoreModule.kt", kt_datastore_module(paths.di_pkg))
            if self.cfg.has_lib("Room"):
                db_pkg = self._resolve_db_pkg()
                write_file(
                    f"{paths.di_dir}/DatabaseModule.kt",
                    kt_room_module(paths.di_pkg, db_pkg, self.cfg.safe_name, self.cfg.db_name),
                )
            # Repository binding module
            write_file(
                f"{paths.di_dir}/RepositoryModule.kt",
                kt_repository_module(paths.di_pkg, paths.repo_iface_pkg, paths.repo_impl_pkg),
            )
            ok("Modules Hilt générés (App, Network, Repository, Database)")

    def _write_room_database(self, paths) -> None:
        """Écrit la classe Room Database, l'Entity et le DAO par défaut."""
        if self.cfg.has_lib("Room"):
            from composeforge.core.writer import pkg_to_path

            pp = pkg_to_path(self.output_dir, self.cfg.package)
            if self.cfg.arch == 0:
                db_dir = f"{pp}/data/local"
                db_pkg = f"{self.cfg.package}.data.local"
            else:
                db_dir = f"{pp}/features/home/data/local"
                db_pkg = f"{self.cfg.package}.features.home.data.local"
            write_file(
                f"{db_dir}/{self.cfg.safe_name}Database.kt",
                kt_room_db(db_pkg, self.cfg.safe_name),
            )
            write_file(f"{db_dir}/AppEntity.kt", kt_room_entity(db_pkg))
            write_file(f"{db_dir}/AppDao.kt", kt_room_dao(db_pkg))
            ok("Room Database, Entity et DAO générés")

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

        write_file(f"{base}/.github/workflows/build.yml", github_actions_ci())
        ok("GitHub Actions CI configuré")

    def _write_test_files(self) -> None:
        """Écrit les fichiers de test (unitaires et instrumentés)."""
        pkg_path = self.cfg.package.replace(".", "/")
        test_dir = os.path.join(
            self.output_dir, "app", "src", "test", "java", *self.cfg.package.split(".")
        )
        android_test_dir = os.path.join(
            self.output_dir, "app", "src", "androidTest", "java", *self.cfg.package.split(".")
        )
        write_file(
            f"{test_dir}/ExampleUnitTest.kt",
            kt_example_unit_test(self.cfg.package),
        )
        write_file(
            f"{android_test_dir}/ExampleInstrumentedTest.kt",
            kt_example_instrumented_test(self.cfg.package),
        )
        ok("Fichiers de test générés (unit + instrumented)")

    # ── Helpers ───────────────────────────────────────

    def _resolve_db_pkg(self) -> str:
        """Résout le package de la Database class selon l'architecture."""
        if self.cfg.arch == 0:
            return f"{self.cfg.package}.data.local"
        return f"{self.cfg.package}.features.home.data.local"
