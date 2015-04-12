from PyQt5.QtWidgets import QSplitter
from PyQt5.QtCore import Qt
from widgets.settings import Settings

class Splitter(QSplitter):
    def __init__(self, parent=None):
        super(QSplitter, self).__init__(parent)
        self.setOrientation(Qt.Horizontal)
        self.setOpaqueResize(True)
        self.setHandleWidth(5)
        self.setChildrenCollapsible(False)
        print(Settings.value("Splitter/state"))

        self.restoreState(Settings.value("Splitter/state"))