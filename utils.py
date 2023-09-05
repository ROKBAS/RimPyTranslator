import os
import tomllib
from pathlib import Path

import tomli_w

DEFAULT_CONFIG = {
    "window": {
        "screen_size": "1280x720",
        "app_position": "0,0",
        "latest_mod_settings_path": "",
    },
    "parser": {
        "ignored_def_tags": [
            {
                "def_name": "FleshTypeDef",
                "tag_list": [
                    "corpseCategory",
                    "damageEffecter",
                    "texture",
                ],
            }
        ],
        "ignored_tag_list": [],
    },
}
TRUES_TYPING = ["True", "False", "TRUE", "FALSE", "true", "false"]
SETTINGS_FILE_NAME = "settings.toml"


def initiate_settings():
    _path = (
        Path(os.path.expanduser("~"))
        .joinpath("RimPyTranslator")
        .joinpath(SETTINGS_FILE_NAME)
    )
    if not os.path.exists(_path):
        with open(_path, "wb") as f:
            tomli_w.dump(DEFAULT_CONFIG, f)
    with open(_path, "rb") as f:
        settings = tomllib.load(f)
    return settings


def save_settings(settings):
    _path = (
        Path(os.path.expanduser("~"))
        .joinpath("RimPyTranslator")
        .joinpath(SETTINGS_FILE_NAME)
    )
    with open(_path, "wb+") as f:
        tomli_w.dump(settings, f)


def open_xml_file(_path):
    with open(_path, "rb") as _file:
        try:
            content = _file.read().decode("utf-8")
        except UnicodeEncodeError:
            try:
                content = _file.read().decode("utf-8-sig")
            except UnicodeDecodeError:
                content = _file.read().decode("utf-16")
    with open(_path, "w+", encoding="utf-8", newline="\n") as _file:
        _file.write(content)
