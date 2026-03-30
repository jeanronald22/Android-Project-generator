"""
composeforge.generator.structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Architecture resolver — maps arch type (0/1/2) to directory structure & package names.
"""

import os
from dataclasses import dataclass

from composeforge.core.config import ProjectConfig
from composeforge.core.writer import pkg_to_path


@dataclass
class ArchitecturePaths:
    """Paths and package names resolved for a given architecture."""

    # Directories (absolute filesystem paths)
    dirs: list
    theme_dir: str
    home_dir: str
    nav_dir: str
    di_dir: str
    core_dir: str
    vm_dir: str
    repo_iface_dir: str
    repo_impl_dir: str
    api_dir: str

    # Package names (Java/Kotlin dotted notation)
    home_pkg: str
    theme_pkg: str
    nav_pkg: str
    di_pkg: str
    core_pkg: str
    vm_pkg: str
    repo_iface_pkg: str
    repo_impl_pkg: str
    api_pkg: str


class ArchitectureResolver:
    """Resolves directory structure and package names for each architecture type."""

    @staticmethod
    def resolve(cfg: ProjectConfig, base_dir: str) -> ArchitecturePaths:
        """Résout les chemins et packages en fonction de l'architecture choisie.

        Args:
            cfg: Project configuration.
            base_dir: Absolute path to the project root directory.

        Returns:
            ArchitecturePaths with all resolved paths and package names.
        """
        pp = pkg_to_path(base_dir, cfg.package)
        pkg = cfg.package

        if cfg.arch == 0:
            return ArchitectureResolver._layered(pp, pkg)
        elif cfg.arch == 1:
            return ArchitectureResolver._feature_based(pp, pkg)
        else:
            return ArchitectureResolver._hybrid(pp, pkg)

    @staticmethod
    def _layered(pp: str, pkg: str) -> ArchitecturePaths:
        """Architecture Layered: data / domain / presentation."""
        return ArchitecturePaths(
            dirs=[
                f"{pp}/data/local/datastore",
                f"{pp}/data/remote/api",
                f"{pp}/data/remote/dto",
                f"{pp}/data/repository",
                f"{pp}/domain/model",
                f"{pp}/domain/repository",
                f"{pp}/domain/usecase",
                f"{pp}/presentation/screens/home",
                f"{pp}/presentation/navigation",
                f"{pp}/presentation/theme",
                f"{pp}/core",
                f"{pp}/di",
            ],
            theme_dir=f"{pp}/presentation/theme",
            home_dir=f"{pp}/presentation/screens/home",
            nav_dir=f"{pp}/presentation/navigation",
            di_dir=f"{pp}/di",
            core_dir=f"{pp}/core",
            vm_dir=f"{pp}/presentation/screens/home",
            repo_iface_dir=f"{pp}/domain/repository",
            repo_impl_dir=f"{pp}/data/repository",
            api_dir=f"{pp}/data/remote/api",
            home_pkg=f"{pkg}.presentation.screens.home",
            theme_pkg=f"{pkg}.presentation.theme",
            nav_pkg=f"{pkg}.presentation.navigation",
            di_pkg=f"{pkg}.di",
            core_pkg=f"{pkg}.core",
            vm_pkg=f"{pkg}.presentation.screens.home",
            repo_iface_pkg=f"{pkg}.domain.repository",
            repo_impl_pkg=f"{pkg}.data.repository",
            api_pkg=f"{pkg}.data.remote.api",
        )

    @staticmethod
    def _feature_based(pp: str, pkg: str) -> ArchitecturePaths:
        """Architecture Feature-based: core + features/..."""
        return ArchitecturePaths(
            dirs=[
                f"{pp}/core/di",
                f"{pp}/core/navigation",
                f"{pp}/core/theme",
                f"{pp}/core/util",
                f"{pp}/features/home/data/remote",
                f"{pp}/features/home/data/repository",
                f"{pp}/features/home/domain/model",
                f"{pp}/features/home/domain/repository",
                f"{pp}/features/home/domain/usecase",
                f"{pp}/features/home/presentation/screens",
                f"{pp}/features/home/presentation/viewmodel",
                f"{pp}/features/home/di",
            ],
            theme_dir=f"{pp}/core/theme",
            home_dir=f"{pp}/features/home/presentation/screens",
            nav_dir=f"{pp}/core/navigation",
            di_dir=f"{pp}/core/di",
            core_dir=f"{pp}/core/util",
            vm_dir=f"{pp}/features/home/presentation/viewmodel",
            repo_iface_dir=f"{pp}/features/home/domain/repository",
            repo_impl_dir=f"{pp}/features/home/data/repository",
            api_dir=f"{pp}/features/home/data/remote",
            home_pkg=f"{pkg}.features.home.presentation.screens",
            theme_pkg=f"{pkg}.core.theme",
            nav_pkg=f"{pkg}.core.navigation",
            di_pkg=f"{pkg}.core.di",
            core_pkg=f"{pkg}.core.util",
            vm_pkg=f"{pkg}.features.home.presentation.viewmodel",
            repo_iface_pkg=f"{pkg}.features.home.domain.repository",
            repo_impl_pkg=f"{pkg}.features.home.data.repository",
            api_pkg=f"{pkg}.features.home.data.remote",
        )

    @staticmethod
    def _hybrid(pp: str, pkg: str) -> ArchitecturePaths:
        """Architecture Hybride: features/feature/{data,domain,presentation}."""
        return ArchitecturePaths(
            dirs=[
                f"{pp}/core/di",
                f"{pp}/core/navigation",
                f"{pp}/core/theme",
                f"{pp}/core/util",
                f"{pp}/core/network",
                f"{pp}/features/home/data/remote/dto",
                f"{pp}/features/home/data/local",
                f"{pp}/features/home/data/repository",
                f"{pp}/features/home/domain/model",
                f"{pp}/features/home/domain/repository",
                f"{pp}/features/home/domain/usecase",
                f"{pp}/features/home/presentation/screens",
                f"{pp}/features/home/presentation/viewmodel",
                f"{pp}/features/home/di",
            ],
            theme_dir=f"{pp}/core/theme",
            home_dir=f"{pp}/features/home/presentation/screens",
            nav_dir=f"{pp}/core/navigation",
            di_dir=f"{pp}/core/di",
            core_dir=f"{pp}/core/util",
            vm_dir=f"{pp}/features/home/presentation/viewmodel",
            repo_iface_dir=f"{pp}/features/home/domain/repository",
            repo_impl_dir=f"{pp}/features/home/data/repository",
            api_dir=f"{pp}/features/home/data/remote",
            home_pkg=f"{pkg}.features.home.presentation.screens",
            theme_pkg=f"{pkg}.core.theme",
            nav_pkg=f"{pkg}.core.navigation",
            di_pkg=f"{pkg}.core.di",
            core_pkg=f"{pkg}.core.util",
            vm_pkg=f"{pkg}.features.home.presentation.viewmodel",
            repo_iface_pkg=f"{pkg}.features.home.domain.repository",
            repo_impl_pkg=f"{pkg}.features.home.data.repository",
            api_pkg=f"{pkg}.features.home.data.remote",
        )

