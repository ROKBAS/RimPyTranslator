import logging
import re
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup as bs
from deep_translator import GoogleTranslator
from lxml import etree
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from gui import Gui
from creation import create_def_xml, create_keyed_xml
from utils import TRUES_TYPING

logger = logging.getLogger(__name__)
parser = etree.XMLParser(remove_comments=True)


class Logic(Gui):  # TODO: Refactor
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

    def analyze_defs(self, root_dir: Path):
        prefered_path, _ = self.working_dirs(root_dir)
        defs_path = root_dir.joinpath("Defs")
        if not defs_path.exists():
            logging.info(f"No defs found in {defs_path}")
            return
        defs_paths = list(Path(defs_path).iterdir())
        defs_names = [str(_.name) for _ in defs_paths]
        if not defs_paths:
            return
        injected_defs = prefered_path.joinpath("DefInjected")
        if not injected_defs.exists():
            injected_defs.mkdir(mode=777, exist_ok=True)
        for def_name, def_path in zip(defs_names, defs_paths):
            local_injected_def_path = injected_defs.joinpath(f"{def_name}")
            self.inject_translation_files(def_path, local_injected_def_path)

    def create_translation_files(
        self, original_file_path: Path, translation_file_path: Path
    ):
        if not str(original_file_path).endswith(".xml"):
            return
        tree = etree.parse(original_file_path, parser)
        root = tree.getroot()
        _defs = root.findall("*")
        if _defs is None:
            return
        for _def in _defs:
            if _def is None:
                continue
            lines = [
                (
                    str(tree.getpath(tag))
                    .replace("]/", ".")
                    .replace("[", ".")
                    .replace("/", ".")
                    .replace("]", ".")
                    .strip()
                    .strip("."),
                    str(tag.text),
                    str(tag.tag),
                )
                for tag in _def.iter()
                if tag is not None
                and str(tag.text) is not None
                and re.sub(r"\s", "", str(tag.text))
                and not re.match("^[-+]?[0-9\.\ ]*$", str(tag.text))
                and str(tag.text) not in TRUES_TYPING
                and str(tag.tag) not in self.ignored_tag_list
            ]
            class_name = _def.find(".//defName")
            if class_name is None:
                class_name = "Unknown Class"
            else:
                class_name = str(class_name.text)
            for _id, string, tag_name in lines:
                found_forbidden_class_bool = False
                for _class in self.ignored_class_list:
                    if _id.find(_class) != -1:
                        found_forbidden_class_bool = True
                        break
                if found_forbidden_class_bool:
                    continue
                if tag_name.find("Def") != -1:
                    continue
                row = self.strings_view.rowCount()
                self.strings_view.insertRow(row)
                _id_item = QTableWidgetItem(_id)
                _id_item.setFlags(Qt.ItemFlag.ItemIsEditable)
                self.strings_view.setItem(row, 0, _id_item)
                _type_item = QTableWidgetItem("Defs")
                _type_item.setFlags(Qt.ItemFlag.ItemIsEditable)
                self.strings_view.setItem(row, 1, _type_item)
                _tag_name_item = QTableWidgetItem(tag_name)
                _tag_name_item.setFlags(Qt.ItemFlag.ItemIsEditable),
                self.strings_view.setItem(row, 2, _tag_name_item)
                cs_name_item = QTableWidgetItem(class_name)
                cs_name_item.setFlags(Qt.ItemFlag.ItemIsEditable)
                self.strings_view.setItem(row, 3, cs_name_item)
                ol_string_item = QTableWidgetItem(string)
                ol_string_item.setFlags(Qt.ItemFlag.ItemIsEditable)
                self.strings_view.setItem(row, 4, ol_string_item)
                self.strings_view.setItem(row, 5, QTableWidgetItem(string))
                of_ph_item = QTableWidgetItem(str(original_file_path))
                of_ph_item.setFlags(Qt.ItemFlag.ItemIsEditable)
                self.strings_view.setItem(row, 6, of_ph_item)
                tf_fp_item = QTableWidgetItem(str(translation_file_path))
                tf_fp_item.setFlags(Qt.ItemFlag.ItemIsEditable)
                self.strings_view.setItem(row, 7, tf_fp_item)

    def inject_translation_files(self, def_path: Path, injected_def_path: Path):
        if def_path.is_dir():  # если оригинальный def папка
            if (
                not injected_def_path.exists()
            ):  # проверить что такая папка не существует в иньекции перевода
                logging.info(f"Creating subfolder in {injected_def_path}")
                injected_def_path.mkdir(mode=777, exist_ok=True)  # создать папку
            defs_paths = list(Path(def_path).iterdir())  # пройдемся по путям в папке
            defs_names = [str(_.name) for _ in defs_paths]  # сформируем нов
            for _def_name, _def_path in zip(defs_names, defs_paths):
                self.inject_translation_files(
                    _def_path, injected_def_path.joinpath(f"{_def_name}")
                )
        elif def_path.is_file():
            self.create_translation_files(def_path, injected_def_path)

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
        with open(original_file_path, "r") as file:
            # Read each line in the file, readlines() returns a list of lines
            content = file.read()
        # Combine the lines in the list into a string
        bs_content = bs(content, features="lxml-xml")
        _LanguageData = bs_content.find("LanguageData")
        if not _LanguageData:
            return
        for _def in _LanguageData.recursiveChildGenerator():
            if not re.sub(r"\s", "", _def.text) or not _def.name:
                continue
            row = self.strings_view.rowCount()
            self.strings_view.insertRow(row)
            self.strings_view.setItem(row, 0, QTableWidgetItem(_def.name))
            self.strings_view.setItem(row, 1, QTableWidgetItem("Keyed"))
            self.strings_view.setItem(row, 2, QTableWidgetItem(_def.text))
            self.strings_view.setItem(row, 3, QTableWidgetItem(str(original_file_path)))
            self.strings_view.setItem(
                row, 4, QTableWidgetItem(str(translation_file_path))
            )

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
