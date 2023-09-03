import logging
import os
import sys

from PySide6.QtWidgets import QApplication

from gui import Gui
from utils import SETTINGS_PATH, initiate_settings

if os.path.exists("RimPyTranslate.log"):
    os.remove("RimPyTranslate.log")

version = "0.2.5"
log_level = logging.DEBUG
logging.basicConfig(
    format="%(levelname)s: %(message)s", level=log_level, filename="RimPyTranslate.log"
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    settings = initiate_settings(SETTINGS_PATH)
    app = QApplication(sys.argv)
    app.setApplicationName("RimPyTranslator")
    width, height = app.screens()[0].size().toTuple()
    main_window = Gui(width, height, settings)
    main_window.show()
    app.exec()
