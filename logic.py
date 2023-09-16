import logging
import os
from pathlib import Path
from typing import List

from deep_translator import GoogleTranslator
from lxml import etree
from PySide6.QtWidgets import QFileDialog

from analyzers.defs import DefAnalyzer
from analyzers.keyed import KeyedAnalyzer
from analyzers.strings import StringsAnalyzer
from creation import create_def_xml, create_keyed_xml
from gui import Gui
from utils import open_xml_file

parser = etree.XMLParser(remove_comments=True)
logger = logging.getLogger(__name__)


class Logic(DefAnalyzer, KeyedAnalyzer, StringsAnalyzer, Gui):
    def __init__(self, width: int, height: int, settings: dict):
        self.show_all_strings = False
        self.settings_mod_folder = ""
        super().__init__(width, height, settings)
        if self.settings["window"].get("latest_mod_settings_path"):
            self.settings_mod_folder = self.settings["window"][
                "latest_mod_settings_path"
            ]
        if not self.settings_mod_folder:
            self.current_mods_folder = (
                Path(os.path.expanduser("~"))
                .joinpath("RimPyTranslator")
                .joinpath("mods")
            )
        else:
            self.current_mods_folder = Path(self.settings_mod_folder)
        self.current_mods_folder.mkdir(mode=511, parents=True, exist_ok=True)
        self.current_mod_path_list: List[str] | None = None
        self.current_mod_list: List[str] | None = None
        self.edit_mods_config_text.setText(f"{self.current_mods_folder}")
        self.open_mods_button.clicked.connect(self.open_file_dialog_mods)
        self.prepare_button.clicked.connect(self.prepare_mod)
        self.translate_button.clicked.connect(self.translate_strings)
        self.patch_button.clicked.connect(self.patch_mod)
        self.allowed_tags_button.clicked.connect(self.add_to_allowed_tags)
        self.filter_cs_button.stateChanged.connect(self.onStateChanged)
        self.original_language = self.original_language_box.currentText()
        self.translation_language = self.translation_language_box.currentText()
        self.pick_mods()

    def onStateChanged(self):
        if self.filter_cs_button.isChecked():
            self.show_all_strings = True
        else:
            self.show_all_strings = False
        self.prepare_mod()

    def add_to_allowed_tags(self):
        for item in self.strings_view.selectedItems():
            self.allowed_tag_list.append(item.text())
            logging.info(f"Added {item.text()} to ignored tags list.")

    def open_file_dialog_mods(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if filenames:
                self.current_mods_folder = Path(filenames[0])
                self.edit_mods_config_text.setText(f"{self.current_mods_folder}")
                self.pick_mods()

    def pick_mods(self):
        directory_pathes = list(Path(self.current_mods_folder).iterdir())
        self.current_mod_path_list = [str(_) for _ in directory_pathes if _.is_dir()]
        self.current_mod_list = [str(_.name) for _ in directory_pathes if _.is_dir()]
        _table_mod_list = []
        for mod_path, file_name in zip(
            self.current_mod_path_list, self.current_mod_list
        ):
            _path_about = Path(mod_path).joinpath("About").joinpath("About.xml")
            open_xml_file(_path_about)
            tree = etree.parse(_path_about, parser)
            root = tree.getroot()
            name = root.find("name")
            if name is not None:
                name = name.text
            else:
                name = "uknown"
            _table_mod_list.append(f"{file_name} | {name}")
        self.file_list.clear()
        self.file_list.addItems(_table_mod_list)

    def prepare_mod(self):
        self.strings_view.clearContents()
        self.strings_view.setRowCount(0)
        for _item in self.file_list.selectedIndexes():
            path = Path(self.current_mod_path_list[_item.row()])
            logging.info(f"Working at {path} on analyzing game mod folders.")
            self.analyze_base_mod(path)

    def translate_strings(self):
        for item in self.strings_view.selectedItems():
            translated = GoogleTranslator(
                source=self.original_language,
                target=self.translation_language,
            ).translate(item.text())
            item.setText(translated)

    def patch_mod(self):
        dictionary_of_strings = {
            "Keyed": {},
            "Defs": {},
            "Strings": {},
        }  # Соритровка с подстановкой
        for row in range(
            self.strings_view.rowCount()
        ):  # Проходимся по итогову списку со строками перевода
            _identifier = self.strings_view.item(
                row, 0
            ).text()  # Строка идентификатора для инъекции перевода
            _type = self.strings_view.item(row, 1).text()  # Тип запаковки
            _text = self.strings_view.item(row, 6).text()  # Итоговый текст
            # OriginalPath = self.strings_view.item(row, 6)
            _futurePath = self.strings_view.item(
                row, 8
            ).text()  # Будующий путь запаковки

            if (
                dictionary_of_strings[_type].get(_futurePath, None) is None
            ):  # Есть ли этот файл в запаковке
                dictionary_of_strings[_type][
                    _futurePath
                ] = []  # Создадим для него место
            dictionary_of_strings[_type][_futurePath].append(
                (_identifier, _text)
            )  # Добавим перевод
        for patch_path in list(dictionary_of_strings["Defs"].keys()):  #
            create_def_xml(dictionary_of_strings["Defs"][patch_path], patch_path)
        for patch_path in list(dictionary_of_strings["Keyed"].keys()):
            create_keyed_xml(dictionary_of_strings["Keyed"][patch_path], patch_path)
        for patch_path in list(dictionary_of_strings["Strings"].keys()):
            logging.warning("Don't know how to patch strings files.")

    def analyze_base_mod(self, path_object: Path):
        for dirpath, dirnames, filenames in os.walk(path_object):
            for dirname in dirnames:
                if dirname == "Defs":
                    self.analyze_defs(Path(dirpath))
                if dirname == "Languages":
                    self.analyze_keyed(Path(dirpath))
                    self.analyze_strings(Path(dirpath))
        logging.info("Analyzed game.")
