import logging
from pathlib import Path

from PySide6.QtWidgets import QTableWidgetItem

from analyzers.base import Analyzer

logger = logging.getLogger(__name__)


class StringsAnalyzer(Analyzer):
    def analyze_strings(self, root_dir: Path):
        prefered_path, creator_path = self.working_dirs(root_dir)
        strings_path = creator_path.joinpath("Strings")
        if not strings_path.exists():
            logging.info(f"No strings found in {strings_path}")
            return
        strings_paths = list(Path(strings_path).iterdir())
        strings_names = [str(_.name) for _ in strings_paths]
        if not strings_paths:
            return
        injected_strings = prefered_path.joinpath("Strings")
        if not injected_strings.exists():
            injected_strings.mkdir(mode=777, exist_ok=True)
        for def_name, def_path in zip(strings_names, strings_paths):
            local_injected_def_path = injected_strings.joinpath(f"{def_name}")
            self.inject_translation_files(def_path, local_injected_def_path)

    def create_translation_files_strings(
        self, original_file_path: Path, translation_file_path: Path
    ):
        pass

    def inject_translation_strings_files(self, def_path: Path, injected_def_path: Path):
        if def_path.is_dir():  # если оригинальный def папка
            if (
                not injected_def_path.exists()
            ):  # проверить что такая папка не существует в иньекции перевода
                logging.info(f"Creating subfolder in {injected_def_path}")
                injected_def_path.mkdir(mode=777, exist_ok=True)  # создать папку
            defs_paths = list(Path(def_path).iterdir())  # пройдемся по путям в папке
            defs_names = [str(_.name) for _ in defs_paths]  # сформируем нов
            for _def_name, _def_path in zip(defs_names, defs_paths):
                self.inject_translation_strings_files(
                    _def_path, injected_def_path.joinpath(f"{_def_name}")
                )
        elif def_path.is_file():
            self.create_translation_files_strings(def_path, injected_def_path)
