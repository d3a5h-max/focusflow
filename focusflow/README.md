# FocusFlow

An independent, offline-first productivity and study-focus application for Android and Windows.

> This repository is a starter foundation, not a finished release. The current prototype includes a basic focus countdown and locally stored tasks. Advanced blocking, usage tracking, cloud sync, multiplayer, and native notification integrations are not implemented yet.

## Current starter features

- Kivy-based cross-platform UI
- 25-minute focus countdown with start, pause, and reset
- Local task list stored in SQLite
- No account or network connection required

## Requirements

- Python 3.10–3.12 recommended
- VS Code
- Git
- Windows: install Python, then `python -m pip install -r requirements.txt`
- Android: Linux or WSL2 is recommended for Buildozer; see `docs/ANDROID_BUILD.md`

## Run on Windows

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

## Build Windows executable

Run `scripts/build_windows.ps1` from PowerShell. The script installs PyInstaller and creates a one-folder build under `dist/`. Test on a clean Windows machine before distributing.

## Android

Buildozer Android packaging is intended to run on Linux/WSL2. See `docs/ANDROID_BUILD.md`. GitHub Actions contains a starter workflow; a successful workflow run is required before calling an APK ready.

## Repository setup

Create a **new private repository named `focusflow`**. Do not rename or reuse `d3a5h-max/pro-pomo`.

```bash
git init
git add .
git commit -m "Initial FocusFlow starter"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/focusflow.git
git push -u origin main
```

## Project status

See `docs/FEATURE_STATUS.md` and `docs/ROADMAP.md`. Feature status is deliberately explicit; planned features must not be represented as implemented.

## Data

The prototype stores tasks in `~/.focusflow/focusflow.sqlite3` on desktop. Android app storage is sandboxed by the platform. Back up important data before testing development builds.
