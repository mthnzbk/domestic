import sys
from PyQt5.QtCore import QSettings,  QFile


if sys.platform == "win32":
    Settings = QSettings("reader.ini", QSettings.IniFormat)
else:
    Settings = QSettings("reader", "reader")


def initial():
    if not QFile.exists(Settings.fileName()):
        pass
        #settings.setValue("Genel/Yol", QDir.homePath())
