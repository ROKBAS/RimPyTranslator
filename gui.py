from pathlib import Path

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from custom_widgets import QHLine
from languages import Languages
from utils import SETTINGS_PATH, save_settings


class Gui(QMainWindow):  # Made GUI Base class for all logic
    def __init__(self, width: int, height: int, settings: dict):
        super().__init__()
        self.setWindowIcon(QIcon("./resources/icon.ico"))
        self.settings = settings
        self.ignored_class_list: list[str] = settings["parser"]["ignored_class_list"]
        self.ignored_tag_list: list[str] = settings["parser"]["ignored_tag_list"]
        _width, _height = self.settings["window"]["screen_size"].split("x")
        _a_x, _a_y = self.settings["window"]["app_position"].split(",")
        self.app_width = int(_width) if _width else width
        self.app_height = int(_height) if _height else height
        self.app_x = int(_a_x) if width else 0
        self.app_y = int(_a_y) if width else 0
        self.setGeometry(self.app_x, self.app_y, self.app_width, self.app_height)
        self._central_widget = QWidget()
        self._central_widget.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        )
        self.setCentralWidget(self._central_widget)
        statusBar = QStatusBar(self._central_widget)
        self.setStatusBar(statusBar)
        self.start_dir = Path(__file__).resolve().parent
        self.file_list = QListWidget(self._central_widget)
        self.strings_view = QTableWidget(self._central_widget)
        self.strings_view.setColumnCount(8)
        self.strings_view.setHorizontalHeaderLabels(
            [
                "Identifier",  # 0
                "Type",  # 1
                "Tag name",  # 2
                "Class name",  # 3
                "Original Text",  # 4
                "Text",  # 5
                "OriginalPath",  # 6
                "FuturePath",  # 7
            ]
        )
        self.current_mods_folder = self.start_dir.joinpath("mods")
        if not self.current_mods_folder.exists():
            self.current_mods_folder.mkdir(mode=777, exist_ok=True)
        mods_toolbar = QToolBar("Mods Folder", self._central_widget)
        self.open_mods_button = QPushButton(text="Select mods folder")
        self.edit_mods_config_text = QLineEdit()
        self.edit_mods_config_text.setText(f"{self.current_mods_folder}")
        mods_toolbar.addWidget(self.open_mods_button)
        mods_toolbar.addWidget(self.edit_mods_config_text)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, mods_toolbar)
        layout = QHBoxLayout(self._central_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.file_list, 1)
        layout.addWidget(self.strings_view, 2)
        self.edit_widget = QWidget()
        layout.addWidget(self.edit_widget)
        self.dev_layout = QFormLayout(self.edit_widget)
        original_language_box = QComboBox(self.edit_widget)
        for item in Languages:
            original_language_box.addItem(item.name)
        translation_language_box = QComboBox(self.edit_widget)
        for item in Languages:
            translation_language_box.addItem(item.name)
        self.prepare_button = QPushButton(text="Prepare", parent=self.edit_widget)
        self.dev_layout.addWidget(self.prepare_button)
        self.translate_button = QPushButton(text="Tranlsate", parent=self.edit_widget)
        self.dev_layout.addWidget(self.translate_button)
        self.patch_button = QPushButton(text="Patch", parent=self.edit_widget)
        self.dev_layout.addWidget(self.patch_button)
        self.dev_layout.addWidget(
            QPushButton(text="Highlight untranslated mods", parent=self.edit_widget)
        )
        self.dev_layout.addWidget(QHLine(parent=self.edit_widget))
        self.dev_layout.addWidget(
            QLabel(text="Selectel original language", parent=self.edit_widget)
        )
        self.dev_layout.addWidget(original_language_box)
        self.dev_layout.addWidget(QHLine(parent=self.edit_widget))
        self.dev_layout.addWidget(
            QLabel(text="Selectel preferred language", parent=self.edit_widget)
        )
        self.dev_layout.addWidget(translation_language_box)
        self.dev_layout.addWidget(QHLine(parent=self.edit_widget))
        settings_widget = QPushButton(text="Options", parent=self.edit_widget)
        settings_widget.setEnabled(False)
        self.dev_layout.addWidget(settings_widget)
        self.current_mod_path_list = None
        self.current_mod_list = None

    def closeEvent(self, event: QCloseEvent):
        self.settings["parser"]["ignored_class_list"] = self.ignored_class_list
        self.settings["parser"]["ignored_tag_list"] = self.ignored_tag_list
        self.settings["window"]["screen_size"] = f"{self.width()}x{self.height()}"
        self.settings["window"]["app_position"] = f"{self.x()},{self.y()}"
        save_settings(self.settings, SETTINGS_PATH)
        event.accept()
