from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from widgets import *
from dialogs import *

class MainWindow(QMainWindow):
    def asd(self, x,y):
        print(self.splitter.sizes())
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setWindowTitle("XXX - {} {}".format(QApplication.applicationName(),QApplication.applicationVersion()))
        self.resize(1000, 600)
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.splitter = Splitter(self.widget)
        self.splitter.splitterMoved.connect(self.asd)
        print(self.splitter.size())
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        #---------------------------------------------------------------
        self.treeWidget = TreeWidget(self.splitter)
        self.toolBox = ToolBox(self.splitter)

        self.page = FirstPage(self.toolBox)
        self.toolBox.addItem(self.page, "")

        self.page2 = LastPage(self.toolBox)
        self.toolBox.addItem(self.page2, "")

        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)
        self.menubar.menuFile.actionExit.triggered.connect(self.close)
        self.menubar.menuFile.menuAdd.actionFeedAdd.triggered.connect(self.feedAdd)
        self.menubar.menuFile.menuAdd.actionFolderAdd.triggered.connect(self.feedFolderAdd)

        self.statusbar = StatusBar(self)
        self.setStatusBar(self.statusbar)
        self.toolBar = ToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBox.currentChanged['int'].connect(self.toolBox.setCurrentIndex)
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), "Yazılar")
        self.toolBox.setItemText(self.toolBox.indexOf(self.page2), "İçerik")

    def closeEvent(self, QCloseEvent):
        Settings.setValue("Splitter/state", self.splitter.saveState())

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
    print(Settings.fileName())
    translator = QTranslator()
    translator.load(os.path.join(QDir.currentPath(), "languages"), "{}".format(LOCALE))
    app.installTranslator(translator)
    app.setApplicationName("Reader")
    app.setApplicationVersion("0.0.1")

    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()