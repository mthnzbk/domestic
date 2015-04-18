import sys
from PyQt5.QtCore import QSettings,  QFile


if sys.platform == "win32":
    Settings = QSettings("Domestic.ini", QSettings.IniFormat)
else:
    Settings = QSettings("Domestic", "Domestic")

def initialSettings():
    if not QFile.exists(Settings.fileName()):
        conftext = r"""[MainWindow]
position=@Point(52 14)
size=@Size(1064 644)

[Splitter]
state=@ByteArray(\0\0\0\xff\0\0\0\x1\0\0\0\x2\0\0\x1\x31\0\0\x2\xf2\0\0\0\0\x5\x1\0\0\0\x1\x1)

[ToolBox]
size=@Size(754 582)

[ToolTreeWidget]
size=@Size(754 520)

[ToolWebView]
size=@Size(754 497)

[TreeWidget]
size=@Size(305 582)

[TreeWidgetHeader]
size0=109
size1=251
size2=70
size3=94
size4=309"""
        with open(Settings.fileName(), "w") as conf:
            conf.write(conftext)
    else: pass
