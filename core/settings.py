import sys
from PyQt5.QtCore import QSettings,  QFile


if sys.platform == "win32":
    Settings = QSettings("Domestic.ini", QSettings.IniFormat)
else:
    Settings = QSettings("Domestic", "Domestic")


def initial():
    if not QFile.exists(Settings.fileName()):
        pass
