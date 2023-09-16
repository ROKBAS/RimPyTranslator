from pathlib import Path

from PySide6.QtCore import QPoint, QSize
from PySide6.QtGui import QCloseEvent, QIcon, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTableWidget,
    QToolBar,
    QWidget,
    QCheckBox,
    QProgressBar,
)

from custom_widgets import QHLine
from languages import Languages
from utils import save_settings


class Gui(QMainWindow):  # Made GUI Base class for all logic
    def __init__(self, width: int, height: int, settings: dict):
        super().__init__()
        self.setWindowIcon(QIcon("./resources/icon.ico"))
        self.settings = settings
        self.allowed_tag_list: list[str] = settings["parser"]["allowed_tag_list"]
        _width, _height = self.settings["window"]["screen_size"].split("x")
        _a_x, _a_y = self.settings["window"]["app_position"].split(",")
        self.app_width = int(_width) if _width else width
        self.app_height = int(_height) if _height else height
        self.app_x = int(_a_x) if width else 0
        self.app_y = int(_a_y) if width else 0
        self.resize(QSize(self.app_width, self.app_height))
        self.move(QPoint(self.app_x, self.app_y))
        self._central_widget = QWidget()
        self._central_widget.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        )
        self.setCentralWidget(self._central_widget)
        self._status_bar = QStatusBar(self._central_widget)
        self.setStatusBar(self._status_bar)
        self.start_dir = Path(__file__).resolve().parent
        self.file_list = QListWidget(self._central_widget)
        self.strings_view = QTableWidget(self._central_widget)
        self.strings_view.setColumnCount(9)
        self.strings_view.setHorizontalHeaderLabels(
            [
                "Identifier",  # 0
                "Type",  # 1
                "Def name",  # 2
                "Tag name",  # 3
                "Class name",  # 4
                "Original Text",  # 5
                "Text",  # 6
                "OriginalPath",  # 7
                "FuturePath",  # 8
            ]
        )
        self.mods_toolbar = QToolBar("Mods Folder", self._central_widget)
        self.open_mods_button = QPushButton(text="Select mods folder")
        self.edit_mods_config_text = QLineEdit()

        self.mods_toolbar.addWidget(self.open_mods_button)
        self.mods_toolbar.addWidget(self.edit_mods_config_text)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.mods_toolbar)
        self._central_layout = QHBoxLayout(self._central_widget)
        self._central_layout.setSpacing(0)
        self._central_layout.setContentsMargins(0, 0, 0, 0)
        self._central_layout.addWidget(self.file_list, 1)
        self._central_layout.addWidget(self.strings_view, 2)
        self.edit_widget = QWidget()
        self._central_layout.addWidget(self.edit_widget)
        self.dev_layout = QFormLayout(self.edit_widget)
        self.original_language_box = QComboBox(self.edit_widget)
        for item in Languages:
            self.original_language_box.addItem(item.name)
        self.translation_language_box = QComboBox(self.edit_widget)
        for item in Languages:
            self.translation_language_box.addItem(item.name)
        self.translation_language_box.setCurrentIndex(1)
        self.prepare_button = QPushButton(text="Prepare", parent=self.edit_widget)
        self.dev_layout.addWidget(self.prepare_button)
        self.translate_button = QPushButton(text="Translate", parent=self.edit_widget)
        self.dev_layout.addWidget(self.translate_button)
        self.patch_button = QPushButton(text="Patch", parent=self.edit_widget)
        self.dev_layout.addWidget(self.patch_button)
        self.filter_cs_button = QCheckBox(
            text="Show all strings", parent=self.edit_widget
        )
        self.filter_cs_button.setChecked(False)
        self.dev_layout.addWidget(self.filter_cs_button)
        self.allowed_tags_button = QPushButton(
            text="Add to allowd tags list", parent=self.edit_widget
        )
        self.dev_layout.addWidget(self.allowed_tags_button)
        self.dev_layout.addWidget(QHLine(parent=self.edit_widget))
        self.dev_layout.addWidget(
            QLabel(text="Selectel original language", parent=self.edit_widget)
        )
        self.dev_layout.addWidget(self.original_language_box)
        self.dev_layout.addWidget(QHLine(parent=self.edit_widget))
        self.dev_layout.addWidget(
            QLabel(text="Selectel preferred language", parent=self.edit_widget)
        )
        self.dev_layout.addWidget(self.translation_language_box)
        self.dev_layout.addWidget(QHLine(parent=self.edit_widget))
        self.statusBar().showMessage("Ready")
        self.progress_bar = QProgressBar(self)
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.setValue(1)

    def closeEvent(self, event: QCloseEvent):
        self.settings["parser"]["allowed_tag_list"] = sorted(self.allowed_tag_list)
        self.settings["window"]["screen_size"] = f"{self.width()}x{self.height()}"
        self.settings["window"]["app_position"] = f"{self.x()},{self.y()}"
        self.settings["window"][
            "latest_mod_settings_path"
        ] = self.edit_mods_config_text.text()
        save_settings(self.settings)
        event.accept()
