import os
import tomllib
import tomli_w

DEFAULT_CONFIG = {
    "window": {"screen_size": "1280x720", "app_position": "0,0"},
    "parser": {"ignored_class_list": [], "ignored_tag_list": []},
}


def initiate_settings(name):
    if not os.path.exists(name):
        with open(name, "wb") as f:
            tomli_w.dump(DEFAULT_CONFIG, f)
    with open(name, "rb") as f:
        settings = tomllib.load(f)
    return settings


def save_settings(settings, path):
    with open(path, "wb+") as f:
        tomli_w.dump(settings, f)
