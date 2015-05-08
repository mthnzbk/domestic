import sys
import os.path as os
from PyQt5.QtCore import QSettings, QFile, QDir, QPoint, QSize


if sys.platform == "win32":
    QDir(QDir.homePath()).mkdir(".domestic-reader")
    Settings = QSettings(os.join(QDir.homePath(), ".domestic-reader","Domestic.ini"), QSettings.IniFormat)
else:
    Settings = QSettings("Domestic", "Domestic")

def initialSettings():
    if not QFile.exists(Settings.fileName()):
        Settings.beginGroup("MainWindow")
        Settings.setValue("position",QPoint(50, 20))
        Settings.setValue("size",QSize(1000, 620))
        Settings.endGroup()
        Settings.beginGroup("TreeWidget")
        Settings.setValue("size",QSize(305, 558))
        Settings.endGroup()
        Settings.beginGroup("ToolBox")
        Settings.setValue("size",QSize(690, 558))
        Settings.endGroup()
        Settings.beginGroup("ToolTreeWidget")
        Settings.setValue("size",QSize(690, 496))
        Settings.endGroup()
        Settings.beginGroup("ToolWebView")
        Settings.setValue("size",QSize(690, 473))
        Settings.endGroup()
        Settings.beginGroup("TreeWidgetHeader")
        Settings.setValue("size0", 100)
        Settings.setValue("size1", 200)
        Settings.setValue("size2", 100)
        Settings.setValue("size3", 100)
        Settings.setValue("size4", 100)
        Settings.endGroup()
        Settings.sync()
