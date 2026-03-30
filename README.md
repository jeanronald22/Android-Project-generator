# 🚀 ComposeForge CLI

> **Android Compose Project Generator** — Scaffolding propre en une commande.

Génère un projet Android complet avec **Jetpack Compose**, **Clean Architecture**, **Material 3**, et les bibliothèques de ton choix.

## ✨ Fonctionnalités

- 🏗 **3 architectures** : Layered, Feature-based, Hybrid
- 📦 **8 bibliothèques** : Hilt, Retrofit, Navigation, Coil, Coroutines, DataStore, Room, Ktor
- 🎨 **Thème Material 3** complet (Light + Dark + Dynamic Color)
- 🧩 **Clean Architecture** : ViewModel, Repository, UseCase, Resource prêts à l'emploi
- 🛡 **DI câblé** : RepositoryModule, NetworkModule, DatabaseModule auto-générés
- 🌲 **Timber** : Logging intégré (debug-only, auto-tag)
- 🎨 **Splash Screen** : API `core-splashscreen` pré-configurée
- 🔄 **CI/CD** : GitHub Actions workflow (build + tests + artifact APK)
- 🧪 **Tests** : JUnit 4, Espresso, Compose UI Tests inclus
- 🔍 **Dry-run** : Prévisualiser l'arborescence avant de générer
- ⚡ **Zéro config** : un projet Android Studio-ready en 30 secondes

## 📋 Prérequis

- Python 3.8+
- Aucune dépendance externe (100% stdlib)

## 🔧 Installation

### Linux / macOS

```bash
# 1. Cloner le projet
git clone <repo-url>
cd Android\ Project\ generator

# 2. Créer un environnement virtuel et installer
python3 -m venv .venv
.venv/bin/pip install -e .

# 3. (Optionnel) Rendre la commande accessible partout
mkdir -p ~/.local/bin
ln -sf "$(pwd)/.venv/bin/composeforge" ~/.local/bin/composeforge

# Si ~/.local/bin n'est pas dans ton PATH :
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Windows

```powershell
# 1. Cloner le projet
git clone <repo-url>
cd "Android Project generator"

# 2. Créer un environnement virtuel et installer
python -m venv .venv
.venv\Scripts\pip install -e .

# 3. Utiliser la commande
.venv\Scripts\composeforge
```

## 🚀 Utilisation

```bash
# Depuis n'importe quel dossier (après installation globale)
composeforge

# Ou directement depuis le dossier du projet
python -m composeforge

# Prévisualiser l'arborescence sans générer
python -m composeforge --dry-run
```

Le wizard te guide en 5 étapes :

1. **Identité** — nom de l'app, package, SDK minimum
2. **Architecture** — Layered / Feature-based / Hybrid
3. **Bibliothèques** — sélection multiple parmi 8 libs populaires
4. **Récapitulatif** — prévisualiser (`p`) ou confirmer (`o`)
5. **Génération** — projet complet prêt pour Android Studio

## 📁 Structure du CLI

```
composeforge/
├── cli/               # Interface utilisateur (couleurs, prompts, affichage)
├── core/              # Config (dataclass), constantes, I/O fichiers
├── templates/         # Templates Gradle, Manifest, Kotlin
│   └── kotlin/        #   Activity, Theme, Screens, ViewModel, Repository,
│                      #   Navigation, DI, Database, Network, Tests, Core
└── generator/         # Moteur de génération + résolution d'architecture
```

## 🏗 Architectures supportées

| Architecture | Structure |
|-------------|-----------|
| **Layered** | `data/` · `domain/` · `presentation/` |
| **Feature-based** | `core/` · `features/home/{data,domain,presentation}` |
| **Hybrid** | `core/{di,navigation,theme,util,network}` · `features/home/{data,domain,presentation}` |

## 📦 Bibliothèques disponibles

| Lib | Description |
|-----|-------------|
| **Hilt** | Injection de dépendances (modules auto-générés) |
| **Retrofit + OkHttp** | Client HTTP avec logging + ApiService exemple |
| **Navigation Compose** | Navigation déclarative + sealed routes |
| **Coil** | Chargement d'images |
| **Coroutines + Flow** | Asynchrone réactif |
| **DataStore** | Préférences persistantes |
| **Room** | Base de données locale (Database + Entity + DAO) |
| **Ktor** | Client HTTP alternatif |

## 🎨 Fichiers générés

Chaque projet inclut :

### Gradle & Config
- ✅ `gradle/libs.versions.toml` — Version catalog
- ✅ `build.gradle.kts` — Racine + App (JVM 2GB heap)
- ✅ `gradle.properties` — JVM args optimisés pour KSP

### Kotlin Source
- ✅ `MainActivity.kt` — Splash Screen + Edge-to-Edge
- ✅ `MyApplication.kt` — Hilt + Timber (debug-only)
- ✅ `HomeScreen.kt` — connecté au ViewModel avec `collectAsStateWithLifecycle`
- ✅ `HomeViewModel.kt` — `@HiltViewModel` + `HomeUiState`
- ✅ `HomeRepository.kt` — interface + impl (avec ApiService si Retrofit)
- ✅ `ApiService.kt` — interface Retrofit avec endpoint exemple
- ✅ Thème Material 3 (`Color.kt`, `Type.kt`, `Theme.kt`)
- ✅ Navigation (`AppNavHost.kt`, `Screen.kt`)
- ✅ Modules Hilt (`AppModule`, `NetworkModule`, `RepositoryModule`, `DatabaseModule`)
- ✅ Core utils (`Resource`, `BaseUseCase`, `BaseViewModel`, `Extensions`)

### Tests & CI
- ✅ `ExampleUnitTest.kt` — Test unitaire JVM
- ✅ `ExampleInstrumentedTest.kt` — Test instrumenté Android
- ✅ `.github/workflows/build.yml` — CI: build + tests + upload APK

### Divers
- ✅ `AndroidManifest.xml`, `.gitignore`, `proguard-rules.pro`, `README.md`

## 📄 Licence

MIT
