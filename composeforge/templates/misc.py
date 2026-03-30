"""
composeforge.templates.misc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Miscellaneous templates: README, .gitignore, proguard, gradle-wrapper.
"""

from composeforge.core.config import ProjectConfig
from composeforge.core.constants import ARCHS


def generate_readme(cfg: ProjectConfig) -> str:
    """Génère README.md."""
    libs_list = "\n".join(f"- {lib}" for lib in cfg.libs) if cfg.libs else "- Aucune bibliothèque supplémentaire"
    arch_label = ARCHS[cfg.arch]

    structure_data = "├── data/          ← Sources de données" if cfg.arch == 0 else "├── core/          ← Modules partagés"
    structure_domain = "├── domain/        ← Logique métier" if cfg.arch == 0 else "├── features/      ← Modules par fonctionnalité"
    structure_pres = "└── presentation/  ← UI (Compose)" if cfg.arch == 0 else "    └── home/"

    return f"""\
# {cfg.app_name}

Projet Android généré automatiquement avec **Android Compose Project Generator**.

## Stack technique

| Composant | Valeur |
|-----------|--------|
| Langage | Kotlin |
| UI | Jetpack Compose + Material 3 |
| Architecture | {arch_label} |
| Min SDK | Android {cfg.min_sdk} |

## Bibliothèques incluses

{libs_list}

## Structure du projet

```
app/src/main/java/{cfg.package.replace('.', '/')}
{structure_data}
{structure_domain}
{structure_pres}
```

## Démarrage rapide

1. Ouvrez le projet dans Android Studio
2. Attendez la synchronisation Gradle
3. Lancez l'app sur un émulateur ou appareil physique

## Personnalisation des couleurs

Éditez `Color.kt` dans le package theme pour adapter la palette à votre marque.
"""


def gitignore() -> str:
    """Génère .gitignore."""
    return (
        "*.iml\n.gradle\n/local.properties\n/.idea\n.DS_Store\n"
        "/build\n/captures\n.externalNativeBuild\n.cxx\nlocal.properties\n"
    )


def proguard() -> str:
    """Génère proguard-rules.pro."""
    return (
        "# Add project specific ProGuard rules here.\n"
        "# For more details, see\n"
        "#   http://developer.android.com/guide/developing/tools/proguard.html\n"
    )


def gradle_wrapper_properties() -> str:
    """Génère gradle/wrapper/gradle-wrapper.properties."""
    return (
        "distributionBase=GRADLE_USER_HOME\n"
        "distributionPath=wrapper/dists\n"
        "distributionUrl=https\\://services.gradle.org/distributions/gradle-8.11.1-bin.zip\n"
        "networkTimeout=10000\n"
        "zipStoreBase=GRADLE_USER_HOME\n"
        "zipStorePath=wrapper/dists\n"
    )


def gradle_properties() -> str:
    """Génère gradle.properties."""
    return (
        "org.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m\n"
        "android.useAndroidX=true\n"
        "kotlin.code.style=official\n"
        "android.nonTransitiveRClass=true\n"
    )


def github_actions_ci() -> str:
    """Génère .github/workflows/build.yml (CI Android)."""
    return """\
name: Android CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
        cache: gradle

    - name: Grant execute permission for gradlew
      run: chmod +x gradlew

    - name: Build with Gradle
      run: ./gradlew assembleDebug

    - name: Run unit tests
      run: ./gradlew testDebugUnitTest

    - name: Upload build artifacts
      uses: actions/upload-artifact@v4
      if: success()
      with:
        name: debug-apk
        path: app/build/outputs/apk/debug/*.apk
        retention-days: 7
"""
