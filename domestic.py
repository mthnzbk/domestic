from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from widgets import *
from dialogs import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setWindowTitle("XXX - {} {}".format(QApplication.applicationName(),QApplication.applicationVersion()))
        self.resize(Settings.value("MainWindow/size"))
        self.move(Settings.value("MainWindow/position"))
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.splitter = Splitter(self.widget)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.treeWidget = TreeWidget(self.splitter)
        self.treeWidget.resize(Settings.value("TreeWidget/size"))
        self.toolBox = ToolBox(self.splitter)
        self.toolBox.resize(Settings.value("ToolBox/size"))

        self.page = FirstPage(self.toolBox)
        self.toolBox.addItem(self.page, "")

        self.page2 = LastPage(self.toolBox)
        self.toolBox.addItem(self.page2, "")
        #self.toolBox.setCurrentIndex(1) # Signal -> currentChanged(0 or 1)

        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)
        self.menubar.menuFile.actionExit.triggered.connect(self.close)
        self.menubar.menuFile.menuAdd.actionFeedAdd.triggered.connect(self.feedAdd)
        self.menubar.menuFile.menuAdd.actionFolderAdd.triggered.connect(self.feedFolderAdd)
        self.menubar.menuHelp.actionAbout.triggered.connect(self.aboutDialog)

        self.statusbar = StatusBar(self)
        self.setStatusBar(self.statusbar)
        self.toolBar = ToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBox.currentChanged['int'].connect(self.toolBox.setCurrentIndex)
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), "Yazılar")
        self.toolBox.setItemText(self.toolBox.indexOf(self.page2), "İçerik")

    def closeEvent(self, QCloseEvent):
        Settings.setValue("Splitter/state", self.splitter.saveState())
        Settings.setValue("MainWindow/size", self.size())
        Settings.setValue("MainWindow/position", self.pos())
        Settings.setValue("TreeWidget/size", self.treeWidget.size())
        Settings.setValue("ToolBox/size",self.toolBox.size())

    def aboutDialog(self):
        about = About(self)
        about.show()

    def feedAdd(self):
        f = FeedAddDialog(self)
        f.show()

    def feedFolderAdd(self):
        f = FeedFolderDialog(self)
        f.show()

def main():
    import sys, os
    app = QApplication(sys.argv)
    LOCALE = QLocale.system().name()
    translator = QTranslator()
    translator.load(os.path.join(QDir.currentPath(), "languages"), "{}".format(LOCALE))
    app.installTranslator(translator)
    app.setApplicationName("Domestic RSS Reader")
    app.setApplicationVersion("0.0.2")

    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()