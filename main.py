import logging
import os
import sys

from PySide6.QtWidgets import QApplication

from logic import Logic
from utils import initiate_settings

if os.path.exists("RimPyTranslate.log"):
    os.remove("RimPyTranslate.log")

version = "1.0.0"
log_level = logging.INFO
logging.basicConfig(
    format="%(levelname)s: %(message)s", level=log_level, filename="RimPyTranslate.log"
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    settings = initiate_settings()
    app = QApplication(sys.argv)
    app.setApplicationName("RimPyTranslator")
    width, height = app.screens()[0].size().toTuple()
    main_window = Logic(width, height, settings)
    main_window.show()
    app.exec()
