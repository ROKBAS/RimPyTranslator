# RimPyTranslator

<!-- ![RimPyTranslator](https://avatars.githubusercontent.com/u/2728043?v=4)
![RimPyTranslator-version]](https://github.com/ROKBAS/RimPyTranslator/releases)
![RimPyTranslator-downloads]](https://github.com/ROKBAS/RimPyTranslator/releases) -->
![License](https://img.shields.io/github/license/ROKBAS/RimPyTranslator)

## Features

- `Translator`: parse files of Mods, extract language files, edit and patch.

## Development

- `Translator`: parse files of Mods, extract language files, edit and patch.

### Structure

- `main`: Startup script, build, run window, start app
- `logic`: Combines main app logic
- `languages`: Languages enum for selecting in gui
- `gui`: General user interface
- `custom_widgets`: Custom widgets for PySide
- `creation`: File creation utilities
- `utils`: Some utility app staff (like save settings)
- `resources`: app resources (img, sounds, etc.)
- `mods`: Default mod folder for source code exec
- `analyzers`: XML Analyzers
- `settings`: app settings

### Run Environment

- Windows (RimPyTranslator.exe)
- Mac OS (RimPyTranslator.zip) currently doesn't know how to build .dmg for mac os

### App development

```bash
python3 -m venv .venv
pip install -r requirements
python main.py
```
