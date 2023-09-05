import logging
import re
from pathlib import Path

from bs4 import BeautifulSoup as bs
from PySide6.QtWidgets import QTableWidgetItem

from analyzers.base import Analyzer

logger = logging.getLogger(__name__)


class KeyedAnalyzer(Analyzer):
    def analyze_keyed(self, root_dir: Path):
        prefered_path, creator_path = self.working_dirs(root_dir)
        keyed_path = creator_path.joinpath("Keyed")
        if not keyed_path.exists():
            logging.info(f"No keyed found in {keyed_path}")
            return
        keyed_paths = list(Path(keyed_path).iterdir())
        keyed_names = [str(_.name) for _ in keyed_paths]
        if not keyed_paths:
            return
        injected_keyed = prefered_path.joinpath("Keyed")
        if not injected_keyed.exists():
            injected_keyed.mkdir(mode=777, exist_ok=True)
        for def_name, def_path in zip(keyed_names, keyed_paths):
            local_injected_def_path = injected_keyed.joinpath(f"{def_name}")
            self.inject_translation_keyed_files(def_path, local_injected_def_path)

    def inject_translation_keyed_files(self, def_path: Path, injected_def_path: Path):
        if def_path.is_dir():  # если оригинальный def папка
            if (
                not injected_def_path.exists()
            ):  # проверить что такая папка не существует в иньекции перевода
                logging.info(f"Creating subfolder in {injected_def_path}")
                injected_def_path.mkdir(mode=777, exist_ok=True)  # создать папку
            defs_paths = list(Path(def_path).iterdir())  # пройдемся по путям в папке
            defs_names = [str(_.name) for _ in defs_paths]  # сформируем новые имена
            for _def_name, _def_path in zip(defs_names, defs_paths):
                self.inject_translation_keyed_files(
                    _def_path, injected_def_path.joinpath(f"{_def_name}")
                )
        elif def_path.is_file():
            self.create_translation_files_keyed(def_path, injected_def_path)

    def create_translation_files_keyed(
        self, original_file_path: Path, translation_file_path: Path
    ):
        if not str(original_file_path).endswith(".xml") and not str(
            original_file_path
        ).endswith(".txt"):
            return
        content = []
        # Read the XML file
        with open(original_file_path, "rb") as file:
            # Read each line in the file, readlines() returns a list of lines
            content = file.read().decode("utf-8")
        _future_LanguageData = None
        if translation_file_path.exists():
            with open(translation_file_path, "rb") as file:
                # Read each line in the file, readlines() returns a list of lines
                future_content = file.read().decode("utf-8")
            future_bs_content = bs(future_content, features="lxml-xml")
            _future_LanguageData = future_bs_content.find("LanguageData")
        bs_content = bs(content, features="lxml-xml")
        _LanguageData = bs_content.find("LanguageData")
        if _future_LanguageData and _LanguageData:
            self.parse_existed_data(
                original_file_path,
                translation_file_path,
                _LanguageData,
                _future_LanguageData,
            )
        elif _LanguageData:
            self.parse_only_native_data(
                original_file_path, translation_file_path, _LanguageData
            )

    def parse_existed_data(
        self,
        original_file_path,
        translation_file_path,
        LanguageData,
        future_LanguageData,
    ):
        _futures_defs = {}
        for _def in future_LanguageData.recursiveChildGenerator():
            if not re.sub(r"\s", "", _def.text) or not _def.name:
                continue
            _futures_defs[_def.name] = _def.text

        for _def in LanguageData.recursiveChildGenerator():
            if not re.sub(r"\s", "", _def.text) or not _def.name:
                continue
            row = self.strings_view.rowCount()
            self.strings_view.insertRow(row)
            self.strings_view.setItem(row, 0, QTableWidgetItem(_def.name))
            self.strings_view.setItem(row, 1, QTableWidgetItem("Keyed"))
            self.strings_view.setItem(row, 2, QTableWidgetItem("-"))
            self.strings_view.setItem(row, 3, QTableWidgetItem("-"))
            self.strings_view.setItem(row, 4, QTableWidgetItem("-"))
            self.strings_view.setItem(row, 5, QTableWidgetItem(_def.text))
            self.strings_view.setItem(
                row,
                6,
                QTableWidgetItem(
                    _futures_defs[_def.name]
                    if _futures_defs.get(_def.name)
                    else _def.text
                ),
            )
            self.strings_view.setItem(row, 7, QTableWidgetItem(str(original_file_path)))
            self.strings_view.setItem(
                row, 8, QTableWidgetItem(str(translation_file_path))
            )

    def parse_only_native_data(
        self, original_file_path, translation_file_path, LanguageData
    ):
        for _def in LanguageData.recursiveChildGenerator():
            if not re.sub(r"\s", "", _def.text) or not _def.name:
                continue
            row = self.strings_view.rowCount()
            self.strings_view.insertRow(row)
            self.strings_view.setItem(row, 0, QTableWidgetItem(_def.name))
            self.strings_view.setItem(row, 1, QTableWidgetItem("Keyed"))
            self.strings_view.setItem(row, 2, QTableWidgetItem("-"))
            self.strings_view.setItem(row, 3, QTableWidgetItem("-"))
            self.strings_view.setItem(row, 4, QTableWidgetItem("-"))
            self.strings_view.setItem(row, 5, QTableWidgetItem(_def.text))
            self.strings_view.setItem(row, 6, QTableWidgetItem(_def.text))
            self.strings_view.setItem(row, 7, QTableWidgetItem(str(original_file_path)))
            self.strings_view.setItem(
                row, 8, QTableWidgetItem(str(translation_file_path))
            )
