import logging
import re
from pathlib import Path
from typing import List

from deep_translator import GoogleTranslator
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from analyzers.defs import DefAnalyzer
from analyzers.keyed import KeyedAnalyzer
from analyzers.strings import StringsAnalyzer
from creation import create_def_xml, create_keyed_xml
from gui import Gui

logger = logging.getLogger(__name__)


class Logic(DefAnalyzer, KeyedAnalyzer, StringsAnalyzer, Gui):  # TODO: Refactor
    def __init__(self, width: int, height: int, settings: dict):
        super().__init__(width, height, settings)
        self.current_mods_folder = self.start_dir.joinpath("mods")
        if not self.current_mods_folder.exists():
            self.current_mods_folder.mkdir(mode=777, exist_ok=True)
        self.current_mod_path_list: List[str] | None = None
        self.current_mod_list: List[str] | None = None
        self.edit_mods_config_text.setText(f"{self.current_mods_folder}")
        self.open_mods_button.clicked.connect(self.open_file_dialog_mods)
        self.prepare_button.clicked.connect(self.prepare_mod)
        self.translate_button.clicked.connect(self.translate_strings)
        self.patch_button.clicked.connect(self.patch_mod)
        self.pick_mods()
        self.prepare_mod()

    def open_file_dialog_mods(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if filenames:
                self.current_mods_folder = Path(filenames[0])
                self.pick_mods()

    def pick_mods(self):
        directory_pathes = list(Path(self.current_mods_folder).iterdir())
        self.current_mod_path_list = [str(_) for _ in directory_pathes if _.is_dir()]
        self.current_mod_list = [str(_.name) for _ in directory_pathes if _.is_dir()]
        self.file_list.clear()
        self.file_list.addItems(self.current_mod_list)

    def prepare_mod(self):
        self.strings_view.clearContents()
        self.strings_view.setRowCount(0)
        for path in self.current_mod_path_list:
            logging.info(f"Working at {path} on analyzing game mod folders.")
            path_object = Path(path)
            self.analyze_base_mod(path_object)
            for version in range(0, 5):
                self.analyze_mod(path_object, f"1.{version}")

    def translate_strings(self):
        current_item = self.strings_view.currentItem()
        translated = GoogleTranslator(source="en", target="ru").translate(
            current_item.text()
        )
        current_item.setText(translated)

    def patch_mod(self):
        dictionary_of_strings = {"Keyed": {}, "Defs": {}, "Strings": {}}
        for row in range(self.strings_view.rowCount()):
            _identifier = self.strings_view.item(row, 0).text()
            _type = self.strings_view.item(row, 1).text()
            _text = self.strings_view.item(row, 5).text()
            # OriginalPath = self.strings_view.item(row, 6)
            _futurePath = self.strings_view.item(row, 7).text()
            if dictionary_of_strings[_type].get(_futurePath, None) is None:
                dictionary_of_strings[_type][_futurePath] = []
            dictionary_of_strings[_type][_futurePath].append((_identifier, _text))
            for patch_path in list(dictionary_of_strings["Defs"].keys()):
                create_def_xml(dictionary_of_strings["Defs"][patch_path], patch_path)
            for patch_path in list(dictionary_of_strings["Keyed"].keys()):
                create_keyed_xml(dictionary_of_strings["Keyed"][patch_path], patch_path)
            for patch_path in list(dictionary_of_strings["Strings"].keys()):
                logging.warning(patch_path)

    def analyze_base_mod(self, path_object: Path):
        if path_object.joinpath("Defs").exists():
            self.analyze_defs(path_object)
        if path_object.joinpath("Languages").exists():
            self.analyze_keyed(path_object)
            self.analyze_strings(path_object)
        logging.info(f"Analyzed base game.")

    def analyze_mod(self, path_object: Path, version: str):
        if path_object.joinpath(version).exists():
            if path_object.joinpath(version).joinpath("Defs").exists():
                self.analyze_defs(path_object.joinpath(version))
            if path_object.joinpath(version).joinpath("Languages").exists():
                self.analyze_keyed(path_object.joinpath(version))
                self.analyze_strings(path_object.joinpath(version))
        logging.info(f"Analyzed version {version}.")
