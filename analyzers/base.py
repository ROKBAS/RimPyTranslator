import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Analyzer:
    def working_dirs(self, path_object: Path):
        languages_path = path_object.joinpath("Languages")
        if not languages_path.exists():
            languages_path.mkdir(mode=777, exist_ok=True)
        prefered_language = languages_path.joinpath("Russian")
        if not prefered_language.exists():
            prefered_language.mkdir(mode=777, exist_ok=True)
        creator_language = languages_path.joinpath("English")
        if not creator_language.exists():
            creator_language.mkdir(mode=777, exist_ok=True)
        return prefered_language, creator_language
