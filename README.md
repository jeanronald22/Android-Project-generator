# 🚀 ComposeForge CLI

> **Android Compose Project Generator** — Scaffolding propre en une commande.

Génère un projet Android complet avec **Jetpack Compose**, **Clean Architecture**, **Material 3**, et les bibliothèques de ton choix.

## ✨ Fonctionnalités

- 🏗 **3 architectures** : Layered, Feature-based, Hybrid
- 📦 **8 bibliothèques** : Hilt, Retrofit, Navigation, Coil, Coroutines, DataStore, Room, Ktor
- 🎨 **Thème Material 3** complet (Light + Dark + Dynamic Color)
- 🧩 **Clean Architecture** : Resource, BaseUseCase, BaseViewModel prêts à l'emploi
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
```

Le wizard te guide en 5 étapes :

1. **Identité** — nom de l'app, package, SDK minimum
2. **Architecture** — Layered / Feature-based / Hybrid
3. **Bibliothèques** — sélection multiple parmi 8 libs populaires
4. **Récapitulatif** — confirmation avant génération
5. **Génération** — projet complet prêt pour Android Studio

## 📁 Structure du CLI

```
composeforge/
├── cli/               # Interface utilisateur (couleurs, prompts, affichage)
├── core/              # Config (dataclass), constantes, I/O fichiers
├── templates/         # Templates Gradle, Manifest, Kotlin
│   └── kotlin/        #   Activity, Theme, Screens, Navigation, DI, Core
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
| **Retrofit + OkHttp** | Client HTTP avec logging |
| **Navigation Compose** | Navigation déclarative + sealed routes |
| **Coil** | Chargement d'images |
| **Coroutines + Flow** | Asynchrone réactif |
| **DataStore** | Préférences persistantes |
| **Room** | Base de données locale (Database + DAO) |
| **Ktor** | Client HTTP alternatif |

## 🎨 Fichiers générés

Chaque projet inclut :

- ✅ `gradle/libs.versions.toml` — Version catalog
- ✅ `build.gradle.kts` — Racine + App
- ✅ `AndroidManifest.xml`
- ✅ `MainActivity.kt` + `MyApplication.kt` (Hilt)
- ✅ Thème Material 3 (`Color.kt`, `Type.kt`, `Theme.kt`)
- ✅ `HomeScreen.kt` avec preview
- ✅ Navigation (`AppNavHost.kt`, `Screen.kt`)
- ✅ Modules Hilt (`AppModule`, `NetworkModule`, `DataStoreModule`, `DatabaseModule`)
- ✅ Core utils (`Resource`, `BaseUseCase`, `BaseViewModel`, `Extensions`)
- ✅ `.gitignore`, `proguard-rules.pro`, `gradle-wrapper.properties`, `README.md`

## 📄 Licence

MIT
