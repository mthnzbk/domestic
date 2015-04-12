from PyQt5.QtWidgets import QMenuBar

from widgets.menu import *


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super(QMenuBar, self).__init__(parent)
        self.menuFile = FileMenu(self)
        self.menuHelp = HelpMenu(self)
        self.menuTools = ToolsMenu(self)
        self.menuFeeds = FeedMenu(self)

        self.addAction(self.menuFile.menuAction())
        self.addAction(self.menuFeeds.menuAction())
        self.addAction(self.menuTools.menuAction())
        self.addAction(self.menuHelp.menuAction())