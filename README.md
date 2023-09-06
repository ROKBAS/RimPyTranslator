# RimPyTranslator

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/ROKBAS/RimPyTranslator/build.yml)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
![GitHub all releases](https://img.shields.io/github/downloads/ROKBAS/RimPyTranslator/total)

## Features

- `Translator`: parse files of Mods, extract language files, edit and patch.

## Install

- Download file from [latest](https://github.com/ROKBAS/RimPyTranslator/releases) release version.
- Download file [`settings.toml`](settings.toml) or replace it like settled in Settings section.

## Use

- PLEASE DOWNLOAD LATEST SETTINGS FROM GITHUB AND REPLACE IT!!!
- Start RimPyTranslator.
- Select mods folder or use contained one from settings.
- Select mod that you need to translate, this column also supports multiselect.
- Press "Prepare" button, this will convert all convertable strings.
- To save your progress between your translation session press "Patch" and after reopening it will open your translated strings.
- Select string from "Translated text" column and translate it, this column also supports multiselect.
- You can press "Translate" button, to help you with selected text translation. (Please select translation original language and preferred).
- When you finished your translation, press "Patch" button, this will create translation files in mod/mods folder/folders.
- You are awesome.

If you see some mess string:

1. Select needed tag in column "Tag name" then use "Add to def ignored tags" button.
2. If you think this tag needs to be ignored globaly use "Add to ignored tags list"

## Settings

- MACOS:

`~/RimPyTranslator` - use `cd ~/RimPyTranslator` on your current user.

- WINDOWS:

`%USERPROFILE%\RimPyTranslator` - you can pass this line to your file exploler.

### Structure

- [`main`](main.py): Startup script, build, run window, start app
- [`logic`](logic.py): Combines main app logic
- [`languages`](languages.py): Languages enum for selecting in gui
- [`gui`](gui.py): General user interface
- [`custom_widgets`](custom_widgets.py): Custom widgets for PySide
- [`creation`](creation): File creation utilities
- [`utils`](utils): Some utility app staff (like save settings)
- [`resources`](resources): app resources (img, sounds, etc.)
- [`analyzers`](analyzers): XML Analyzers
- [`settings.toml`](settings.toml): app settings

### Run Environment

- Windows (RimPyTranslator.exe)
- Mac OS (RimPyTranslator.zip):
    1. Supported all versions (ARM, Intel).
    2. Doesn't know how to build .dmg for mac os, just use it like `./RimPyTranslator`
- Linux:
    1. Work in progress

### App development

```bash
python3 -m venv .venv
pip install -r requirements
python main.py
```
