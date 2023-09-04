# RimPyTranslator

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/ROKBAS/RimPyTranslator/build.yml)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
![GitHub all releases](https://img.shields.io/github/downloads/ROKBAS/RimPyTranslator/total)

## Features

- `Translator`: parse files of Mods, extract language files, edit and patch.

## Install

- Download file from [latest](https://github.com/ROKBAS/RimPyTranslator/releases) release version.
- Download file [`settings.toml`](settings.xml) or replace it like settled in Settings section.

## Use

- PLEASE DOWNLOAD LATEST SETTINGS FROM GITHUB AND REPLACE IT!!!
- Start RimPyTranslator.
- Select mods folder or use contained one from settings.
- Select mod that you need to translate.
- Press "Prepare" button, this will convert all convertable strings.
- Select string from "Translated text" column and translate it.
- Press "Translate" button, to help you with selected text translation.
- When you finished your translation, press "Patch" button, this will create translation files in mod folder.
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
- Mac OS (RimPyTranslator.zip):

    1. Currently supported all versions (ARM, Intel).
    2. currently doesn't know how to build .dmg for mac os, just use  it like `./RimPyTranslator`

### App development

```bash
python3 -m venv .venv
pip install -r requirements
python main.py
```
