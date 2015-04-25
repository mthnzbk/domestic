#!/usr/bin/env python3
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from widgets import *
from dialogs import *
from core import ReaderDb, Settings, FeedSync, initialSettings, initialDb
import resource

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.resize(Settings.value("MainWindow/size"))
        self.move(Settings.value("MainWindow/position"))
        self.setWindowTitle()
        self.setWindowIcon(QIcon(":/images/rss-icon-128.png"))
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.splitter = QSplitter(self.widget)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(5)
        self.splitter.setChildrenCollapsible(False)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.treeWidget = TreeWidget(self.splitter)
        self.treeWidget.setFocus()
        self.treeWidget.resize(Settings.value("TreeWidget/size"))

        self.toolBox = ToolBox(self.splitter)
        self.toolBox.resize(Settings.value("ToolBox/size"))
        self.page = FirstPage(self.toolBox)
        self.toolBox.addItem(self.page, "")

        self.page2 = LastPage(self.toolBox)

        self.toolBox.addItem(self.page2, "")
        #self.toolBox.setCurrentIndex(1) # Signal -> currentChanged(0 or 1)
        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.menuFile = FileMenu(self)
        self.menuHelp = HelpMenu(self)
        self.menuTools = ToolsMenu(self)
        self.menuFeeds = FeedMenu(self)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuFeeds.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.statusbar = StatusBar(self)
        self.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(self)
        self.toolBar.setMovable(False)
        self.toolBar.addActions((self.menuFile.menuAdd.actionFeedAdd, self.menuFile.menuAdd.actionFolderAdd))
        self.toolBar.addSeparator()
        self.toolBar.addActions((self.menuFeeds.actionAllUpdate, self.menuFeeds.actionStoreAdd, self.menuFeeds.actionDelete))
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.menuFeeds.actionInfo)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBox.setItemText(self.toolBox.indexOf(self.page), "Yazılar")
        self.toolBox.setItemText(self.toolBox.indexOf(self.page2), "İçerik")

        self.treeWidget.treeWidgetTitleSignal.connect(self.setWindowTitle)

        self.menuFile.actionExit.triggered.connect(self.close)
        self.menuFile.menuAdd.actionFeedAdd.triggered.connect(self.feedAdd)
        self.menuFile.menuAdd.actionFolderAdd.triggered.connect(self.feedFolderAdd)

        self.menuHelp.actionAbout.triggered.connect(self.aboutDialog)
        self.menuFeeds.actionDelete.triggered.connect(self.feedDelete)
        self.menuFeeds.actionStoreAdd.triggered.connect(self.feedStore)
        self.menuFeeds.actionAllUpdate.triggered.connect(self.allUpdate)
        self.menuFeeds.actionInfo.triggered.connect(self.feedInfoDialog)

        self.treeWidget.unreadFolderClicked.connect(self.page.entryList)
        self.treeWidget.deletedFolderClicked.connect(self.page.entryList)
        self.treeWidget.storeFolderClicked.connect(self.page.entryList)

    def sync(self): # açılış ve sinyalle  MainWindowu güncelleme
        self.treeWidget.clear()
        self.treeWidget.widgetInitial()
        self.treeWidget.allFolderAndFeed()
        self.treeWidget.unreadFolderInıt()
        self.treeWidget.deletedFolderInıt()
        self.treeWidget.storeFolderInıt()
        self.menuFeeds.actionAllUpdate.setEnabled(True)

    def closeEvent(self, event):
        Settings.setValue("MainWindow/size", self.size())
        Settings.setValue("MainWindow/position", self.pos())
        Settings.setValue("TreeWidget/size", self.treeWidget.size())
        Settings.setValue("ToolBox/size",self.toolBox.size())
        Settings.setValue("TreeWidgetHeader/size0",self.page.treeWidget.header().sectionSize(0))
        Settings.setValue("TreeWidgetHeader/size1",self.page.treeWidget.header().sectionSize(1))
        Settings.setValue("TreeWidgetHeader/size2",self.page.treeWidget.header().sectionSize(2))
        Settings.setValue("TreeWidgetHeader/size3",self.page.treeWidget.header().sectionSize(3))
        Settings.setValue("TreeWidgetHeader/size4",self.page.treeWidget.header().sectionSize(4))
        Settings.setValue("ToolTreeWidget/size", self.page.treeWidget.size())
        Settings.setValue("ToolWebView/size", self.page2.browser.size())

    def setWindowTitle(self, title=None):
        if title != None:
            super(MainWindow, self).setWindowTitle("{} - {} {}".format(title, QApplication.applicationName(),QApplication.applicationVersion()))
        else:
            super(MainWindow, self).setWindowTitle("{} {}".format(QApplication.applicationName(),QApplication.applicationVersion()))

    def allUpdate(self):
        self.menuFeeds.actionAllUpdate.setEnabled(False)
        db = ReaderDb()
        control = db.execute("select url from feeds")
        feedList = control.fetchall()
        thread = FeedSync(self)
        thread.feedAdd(feedList)
        thread.start()
        thread.finished.connect(self.sync)

    def feedDelete(self):
        if self.page.treeWidget.hasFocus():
            itemAll = self.page.treeWidget.selectedItems()
            item_list = [(item.getEntryUrl(),) for item in itemAll]
            print(item_list)
            db = ReaderDb()
            if itemAll != None:
                if self.treeWidget.currentItem() == self.treeWidget.unreadFolder or self.treeWidget.currentItem() == self.treeWidget.storeFolder:
                    db.executemany("update store set istrash=1, iscache=0, isstore=0 where entry_url=?", item_list)
                    db.commit()
                    db.close()
                if self.treeWidget.currentItem() == self.treeWidget.deletedFolder:
                    db.executemany("update store set istrash=-1, iscache=0, isstore=0 where entry_url=?", item_list)
                    db.commit()
                    db.close()
                if self.treeWidget.currentItem() == self.treeWidget.unreadFolder:
                    print(self.page.treeWidget.currentColumn())
                    self.treeWidget.unreadFolderClick()
                    self.treeWidget.deletedFolderInıt()
                elif self.treeWidget.currentItem() == self.treeWidget.storeFolder:
                    self.treeWidget.storeFolderClick()
                    self.treeWidget.deletedFolderInıt()
                elif self.treeWidget.currentItem() == self.treeWidget.deletedFolder:
                    self.treeWidget.deletedFolderClick()
            else:
                print("Seçim yapılmamış!")
        elif self.treeWidget.hasFocus():
            print("Yanlış yapıyorsun!")
        else:
            print("Hıamına!")

    def feedStore(self):
        if self.page.treeWidget.hasFocus():
            itemAll = self.page.treeWidget.selectedItems()
            item_list = [(item.getEntryUrl(),) for item in itemAll]
            db = ReaderDb()
            if itemAll != None:
                if self.treeWidget.currentItem() == self.treeWidget.unreadFolder or self.treeWidget.currentItem() == self.treeWidget.deletedFolder:
                    db.executemany("update store set istrash=0, iscache=0, isstore=1 where entry_url=?", item_list)
                    db.commit()
                    db.close()
                if self.treeWidget.currentItem() == self.treeWidget.storeFolder:
                    print("Bunları saklayamazsın. Zaten saklamışsın!")
                if self.treeWidget.currentItem() == self.treeWidget.unreadFolder:
                    self.treeWidget.unreadFolderClick()
                    self.treeWidget.storeFolderInıt()
                elif self.treeWidget.currentItem() == self.treeWidget.deletedFolder:
                    self.treeWidget.deletedFolderClick()
                    self.treeWidget.storeFolderInıt()
            else:
                print("Seçim yapılmamış!")
        elif self.treeWidget.hasFocus():
            print("Yanlış yapıyorsun!")
        else:
            print("Hıamına!")

    def feedInfoDialog(self):
        pass

    def aboutDialog(self):
        about = About(self)
        about.show()

    def feedAdd(self):
        f = RSSAddDialog(self)
        f.rssAddFinished.connect(self.allUpdate)
        f.show()

    def feedFolderAdd(self):
        f = RSSFolderDialog(self)
        f.folderAddFinished.connect(self.sync)
        f.show()

def main():
    import sys, os
    app = QApplication(sys.argv)
    LOCALE = QLocale.system().name()
    translator = QTranslator()
    translator.load(os.path.join(QDir.currentPath(), "languages"), "{}".format(LOCALE))
    app.installTranslator(translator)
    app.setApplicationName(app.tr("Domestic RSS Okuyucu"))
    app.setApplicationVersion("0.0.3.1")

    initialSettings()
    initialDb()

    """sharedMemory = QSharedMemory("f33a4b06-72f5-4b72-90f4-90d606cdf98c")
    if sharedMemory.create(512, QSharedMemory.ReadWrite) == False:
        sys.exit()"""

    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
