import logging
import re
from pathlib import Path

from lxml import etree
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem

from analyzers.base import Analyzer
from utils import TRUES_TYPING

logger = logging.getLogger(__name__)
parser = etree.XMLParser(remove_comments=True)


class DefAnalyzer(Analyzer):
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
            lines = []
            for tag in _def.iter():
                if (
                    tag is not None
                    and str(tag.text) is not None
                    and re.sub(r"\s", "", str(tag.text))
                    and not re.match("^[-+]?[0-9\.\ ]*$", str(tag.text))
                    and str(tag.text) not in TRUES_TYPING
                    and str(tag.tag) not in self.ignored_tag_list
                    and str(tag.getparent().tag) not in self.ignored_tag_list
                ):
                    class_name = _def.find(".//defName")
                    if class_name is None:
                        class_name = str(tag.getparent().tag)
                    else:
                        class_name = str(class_name.text)
                    _id_of_sected_tag = str(tree.getpath(tag)).replace("]/", ".").replace("[", ".").replace("/", ".").replace("]", ".").strip().strip(".") # Containts Def. at start
                    lines.append(
                        (
                            _id_of_sected_tag[5:],
                            str(tag.text),
                            str(tag.tag)
                            if str(tag.tag) != "li"
                            else str(tag.getparent().tag),
                        )
                    )
            for _id, string, tag_name in lines:
                found_forbidden_tag_in_class_bool = False
                for _def_name, _tag_def_list in self.ignored_def_tags.items():
                    if _id.find(_def_name) > -1:
                        for _tag in _tag_def_list:
                            if _id.find(_tag) != -1:
                                found_forbidden_tag_in_class_bool = True
                                break
                    if found_forbidden_tag_in_class_bool:
                        break
                if found_forbidden_tag_in_class_bool:
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
                # _tag_name_item.setFlags(Qt.ItemFlag.ItemIsEnabled),
                self.strings_view.setItem(row, 2, _tag_name_item)
                cs_name_item = QTableWidgetItem(class_name)
                # cs_name_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
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
