# RimPyTranslator
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/ROKBAS/RimPyTranslator/build.yml)
![License](https://img.shields.io/github/license/ROKBAS/RimPyTranslator)
![GitHub all releases](https://img.shields.io/github/downloads/ROKBAS/RimPyTranslator/total)

## Features

- `Translator`: parse files of Mods, extract language files, edit and patch.

## Install

- Download file from latets release version
- Download file `settings.toml` or replace it like settled in Settings section

## Use

- Start RimPyTranslator.
- Select mods folder or use contained one from settings.
- Select mod that you need to translate.
- Press "Prepare" button, this will convert all convertable strings.

If you see some mess string:

1. Select needed tag in column "Tag name" then use "Add to def ignored tags" button.
2. If you think this tag needs to be ignored globaly use "Add to ignored tags list"

## Settings

- MACOS:

`~/RimPyTranslator` - use `cd ~/RimPyTranslator` on your current user.

- WINDOWS:

`%USERPROFILE%\RimPyTranslator` - you can pass this line to your file exploler.

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
