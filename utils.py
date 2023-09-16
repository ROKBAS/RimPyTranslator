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
        "allowed_tag_list": [
            "ReportStringPatrolling",
            "approachOrderString",
            "approachingReportString",
            "arrivalTextEnemy",
            "arrivalTextExtra",
            "arrivedLetter",
            "baseDesc",
            "baseDescription",
            "baseInspectLine",
            "beginLetter",
            "beginRitualOverride",
            "calledOffMessage",
            "customChildDisallowMessage",
            "customLabel",
            "deathMessage",
            "description",
            "descriptionExtra",
            "descriptionFuture",
            "descriptionShort",
            "destroyedLabel",
            "destroyedOutLabel",
            "effectDesc",
            "endMessage",
            "extraTooltip",
            "finishedMessage",
            "fixedName",
            "formatString",
            "gerund",
            "gerundLabel",
            "graphLabelY",
            "headerTip",
            "helpText",
            "ingestCommandString",
            "ingestReportString",
            "jobReportOverride",
            "jobString",
            "label",
            "labelAbstract",
            "labelFemale",
            "labelFemalePlural",
            "labelName",
            "labelNoun",
            "labelNounPretty",
            "labelPlural",
            "labelPrefix",
            "labelShort",
            "labelShortAdj",
            "leaderDescription",
            "leaderTitle",
            "letterInfoText",
            "letterLabel",
            "letterLabelEnemy",
            "letterLabelFriendly",
            "letterText",
            "letterTitle",
            "message",
            "noCandidatesGizmoDesc",
            "notifyMessage",
            "noun",
            "overrideLabel",
            "pawnLabel",
            "pawnSingular",
            "pawnsPlural",
            "permanentLabel",
            "recoveryMessage",
            "rejectInputMessage",
            "reportString",
            "royalFavorLabel",
            "rulesStrings",
            "spectatorGerund",
            "spectatorsLabel",
            "text",
            "textController",
            "textEnemy",
            "textFriendly",
            "textWillArrive",
            "thoughtStageDescriptions",
            "title",
            "titleFemale",
            "titleShort",
            "titleShortFemale",
            "valueFormat",
            "verb",
        ],
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
