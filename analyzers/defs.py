import logging
import re
from pathlib import Path

from lxml import etree
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem

from analyzers.base import Analyzer
from utils import TRUES_TYPING, open_xml_file

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
        for _, def_path in zip(defs_names, defs_paths):
            self.inject_translation_files(def_path, injected_defs)

    def create_translation_files(
        self, original_file_path: Path, translation_file_path: Path
    ):
        if not str(original_file_path).endswith(".xml"):
            return
        open_xml_file(original_file_path)
        tree = etree.parse(original_file_path, parser)
        root = tree.getroot()
        _defs = root.findall("*")
        if _defs is None:
            return
        for _def in _defs:
            lines = []
            for tag in _def.iter():
                if (
                    tag is not None
                    and str(tag.text) is not None
                    and re.sub(r"\s", "", str(tag.text))
                    and not re.match("^[-+]?[0-9\.\ ]*$", str(tag.text))
                    and str(tag.text) not in TRUES_TYPING
                ):
                    class_name = _def.find(".//defName")
                    if class_name is None:
                        class_name = str(tag.getparent().tag)
                    else:
                        class_name = str(class_name.text)
                    _id_of_sected_tag = (
                        str(tree.getelementpath(tag))
                        .replace("]/", ".")
                        .replace("[", ".")
                        .replace("/", ".")
                        .replace("]", ".")
                        .strip()
                        .strip(".")
                    )

                    _base_def_name = str(_def.tag)  # Base def
                    _id_of_sected_tag = f"{class_name}.{_id_of_sected_tag}"
                    _def_index = _id_of_sected_tag.find("Def")
                    if _def_index == -1:
                        _def_index = _id_of_sected_tag.find("def")
                    _id_of_sected_tag = _id_of_sected_tag[_def_index + 3 :]
                    _id_of_sected_tag = f"{class_name}{_id_of_sected_tag}"
                    _split_id = _id_of_sected_tag.split(".")
                    if len(_split_id) > 1 and _split_id[1].isdigit():
                        del _split_id[1]
                    _id_of_sected_tag = ".".join(_split_id)
                    _split_id = _id_of_sected_tag.split(".")
                    for num, value in enumerate(_split_id):
                        if value.isdigit():
                            _split_id[num] = str(int(value) - 1)
                    _id_of_sected_tag = ".".join(_split_id)
                    while _id_of_sected_tag.find(".li.") > -1:
                        _idx_of_li = _id_of_sected_tag.find(
                            ".li."
                        )  # index of li elemnt
                        _after_li_string = _id_of_sected_tag[
                            _idx_of_li + 4 : len(_id_of_sected_tag)
                        ]
                        if _after_li_string.split(".")[0].isdigit():
                            _id_of_sected_tag = (
                                _id_of_sected_tag[: _idx_of_li + 1] + _after_li_string
                            )
                        else:
                            _id_of_sected_tag = (
                                _id_of_sected_tag[:_idx_of_li]
                                + ".0."
                                + _after_li_string
                            )

                    _tag_name = (
                        str(tag.tag)
                        if str(tag.tag) != "li"
                        else str(tag.getparent().tag)
                    )
                    if _tag_name in self.ignored_tag_list:
                        continue
                    lines.append(
                        (
                            _id_of_sected_tag,
                            str(tag.text),
                            _tag_name,
                            class_name,
                            _base_def_name,
                            translation_file_path.joinpath(_base_def_name).joinpath(
                                original_file_path.name
                            ),
                        )
                    )
            if not lines:
                return
            self.translate_mixed(original_file_path, lines)

    def translate_mixed(self, original_file_path, lines):
        for (
            _id,
            string,
            tag_name,
            class_name,
            base_def_name,
            translation_file_path,
        ) in lines:
            _future_root = None
            if translation_file_path.exists():
                open_xml_file(translation_file_path)
                _future_tree = etree.parse(translation_file_path, parser)
                _future_root = _future_tree.getroot()
            found_forbidden_tag_in_class_bool = False
            for _def_name, _tag_def_list in self.ignored_def_tags.items():
                if base_def_name.find(_def_name) > -1:
                    for _tag in _tag_def_list:
                        if tag_name.find(_tag) != -1:
                            found_forbidden_tag_in_class_bool = True
                            break
                if found_forbidden_tag_in_class_bool:
                    break
            if found_forbidden_tag_in_class_bool:
                continue
            _existing_def = None
            if _future_root:
                _existing_def = _future_root.find(_id)
            row = self.strings_view.rowCount()
            self.strings_view.insertRow(row)
            _id_item = QTableWidgetItem(_id)
            _id_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            self.strings_view.setItem(row, 0, _id_item)
            _type_item = QTableWidgetItem("Defs")
            _type_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            self.strings_view.setItem(row, 1, _type_item)
            _def_name_item = QTableWidgetItem(base_def_name)
            self.strings_view.setItem(row, 2, _def_name_item)
            _tag_name_item = QTableWidgetItem(tag_name)
            self.strings_view.setItem(row, 3, _tag_name_item)
            cs_name_item = QTableWidgetItem(class_name)
            self.strings_view.setItem(row, 4, cs_name_item)
            ol_string_item = QTableWidgetItem(string)
            ol_string_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            self.strings_view.setItem(row, 5, ol_string_item)
            if _existing_def is not None and len(_existing_def.text) >= 0:
                string = _existing_def.text
            self.strings_view.setItem(row, 6, QTableWidgetItem(string))
            of_ph_item = QTableWidgetItem(str(original_file_path))
            of_ph_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            self.strings_view.setItem(row, 7, of_ph_item)
            tf_fp_item = QTableWidgetItem(str(translation_file_path))
            tf_fp_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            self.strings_view.setItem(row, 8, tf_fp_item)

    def inject_translation_files(self, def_path: Path, injected_def_path: Path):
        if def_path.is_dir():  # если оригинальный def папка
            defs_paths = list(Path(def_path).iterdir())  # пройдемся по путям в папке
            defs_names = [str(_.name) for _ in defs_paths]  # сформируем нов
            for _, _def_path in zip(defs_names, defs_paths):
                self.inject_translation_files(_def_path, injected_def_path)
        elif def_path.is_file():
            self.create_translation_files(def_path, injected_def_path)
