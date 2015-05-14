#!/usr/bin/env python3
import sys, os.path as os
from xml.etree import cElementTree
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from domestic.widgets import *
from domestic.dialogs import *
from domestic.core import ReaderDb, Settings, FeedSync, initialSettings, initialDb
from domestic import resource

mainPath = os.abspath(os.dirname(__file__))

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
        self.splitter.setHandleWidth(1)
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

        self.toolBox.setItemText(self.toolBox.indexOf(self.page), self.tr("Entries"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page2), self.tr("Content"))

        self.treeWidget.treeWidgetTitleSignal.connect(self.setWindowTitle)

        self.menuFile.actionExit.triggered.connect(self.close)
        self.menuFile.actionExport.triggered.connect(self.exportFileDialog)
        self.menuFile.actionImport.triggered.connect(self.importFileDialog)
        self.menuFile.menuAdd.actionFeedAdd.triggered.connect(self.feedAdd)
        self.menuFile.menuAdd.actionFolderAdd.triggered.connect(self.feedFolderAdd)

        self.menuHelp.actionAbout.triggered.connect(self.aboutDialog)
        self.menuFeeds.actionDelete.triggered.connect(self.feedDelete)
        self.menuFeeds.actionStoreAdd.triggered.connect(self.feedStore)
        self.menuFeeds.actionAllUpdate.triggered.connect(self.allUpdate)
        self.menuFeeds.actionInfo.triggered.connect(self.infoDialog)

        self.treeWidget.unreadFolderClicked.connect(self.page.entryList)
        self.treeWidget.deletedFolderClicked.connect(self.page.entryList)
        self.treeWidget.storeFolderClicked.connect(self.page.entryList)

        self.treeWidget.setFocus()

    def sync(self, sync=False):
        if sync:
            self.treeWidget.clear()
            self.treeWidget.widgetInitial()
            self.treeWidget.categorySorting(treeitem=self.treeWidget)
            self.treeWidget.deletedFolderInit()
            self.treeWidget.storeFolderInit()
            self.treeWidget.setCurrentItem(self.treeWidget.unreadFolder)
            self.treeWidget.setFocus()
            self.treeWidget.unreadFolderClick()

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
            super(MainWindow, self).setWindowTitle("{} {}".format(QApplication.applicationName(), QApplication.applicationVersion()))

    def feedUpdate(self, feedurl=None):
        db = ReaderDb()
        control = db.execute("select feed_url from folders where type='feed' and feed_url=?", (feedurl,))
        feed = control.fetchone()
        thread = FeedSync(self)
        thread.feedAdd(feed)
        thread.start()
        thread.isData.connect(self.sync)

    def allUpdate(self):
        QApplication.setOverrideCursor(Qt.BusyCursor)
        db = ReaderDb()
        control = db.execute("select feed_url from folders where type='feed'")
        feedList = control.fetchall()
        self.statusbar.progress.setMaximum(len(feedList))
        for feedurl in feedList:
            thread = FeedSync(self)
            thread.feedAdd(feedurl)
            thread.start()
            thread.isData.connect(self.notifySoundPlay)
            thread.isData.connect(self.sync)
            thread.isData.connect(self.statusbar.setProgress)

    def notifySoundPlay(self, datain):
        if datain:
            media = QMediaPlayer(self)
            media.setMedia(QMediaContent(QUrl.fromLocalFile(os.join(mainPath, "media", "notify.mp3"))))
            media.setVolume(100)
            media.play()

    def feedDelete(self):
        if self.page.treeWidget.hasFocus():
            itemAll = self.page.treeWidget.selectedItems()
            item_list = [(item.getEntryUrl(),) for item in itemAll]
            db = ReaderDb()
            if itemAll != None:
                if self.treeWidget.currentItem() == self.treeWidget.unreadFolder or self.treeWidget.currentItem() == self.treeWidget.storeFolder:
                    db.executemany("update store set istrash=1, iscache=0, isstore=0 where entry_url=?", item_list)
                    db.commit()
                    db.close()
                if self.treeWidget.currentItem() == self.treeWidget.deletedFolder:
                    db.executemany("update store set istrash=-1, iscache=0, isstore=0, entry_content='' where entry_url=?", item_list)
                    db.commit()
                    db.close()
                if self.treeWidget.currentItem() == self.treeWidget.unreadFolder:
                    self.treeWidget.unreadFolderClick()
                    self.treeWidget.deletedFolderInit()
                elif self.treeWidget.currentItem() == self.treeWidget.storeFolder:
                    self.treeWidget.storeFolderClick()
                    self.treeWidget.deletedFolderInit()
                elif self.treeWidget.currentItem() == self.treeWidget.deletedFolder:
                    self.treeWidget.deletedFolderClick()
                else:
                    QMessageBox.warning(self, self.tr("Warning!"), self.tr("Selection has not done!"))
        elif self.treeWidget.hasFocus():
            items = self.treeWidget.selectedItems()
            if len(items):
                for item in items:
                    if isinstance(item, FeedItem):
                        box = QMessageBox.question(self, self.tr("Are you sure?"),
                                                   self.tr("Do you want to delete the {} feed?").format(item.title))
                        if box == 16384:
                            db = ReaderDb()
                            db.execute("delete from folders where feed_url=?", (item.feed_url,))
                            db.commit()
                            db.close()
                            self.sync(True)
                    if isinstance(item, FolderItem):
                        db = ReaderDb()
                        db.execute("select * from folders where parent=?", (item.id,))
                        if db.cursor.fetchone():
                            QMessageBox.warning(self, self.tr("Warning!"), self.tr("Before, you empty for the directory!"))
                        else:
                            db.execute("delete from folders where id=?", (item.id,))
                            db.commit()
                            self.sync(True)
                        db.close()
        else:
            QMessageBox.warning(self, self.tr("Warning!"), self.tr("Selection has not done!"))

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
                if self.treeWidget.currentItem() == self.treeWidget.storeFolder and len(itemAll) > 0:
                    QMessageBox.warning(self, self.tr("Warning!"), self.tr("These are already stored."))
                elif self.treeWidget.currentItem() == self.treeWidget.unreadFolder:
                    self.treeWidget.unreadFolderClick()
                    self.treeWidget.storeFolderInit()
                elif self.treeWidget.currentItem() == self.treeWidget.deletedFolder:
                    self.treeWidget.deletedFolderClick()
                    self.treeWidget.storeFolderInit()
                else:
                    QMessageBox.warning(self, self.tr("Warning!"), self.tr("Selection has not done!"))
        else:
            QMessageBox.warning(self, self.tr("Warning!"), self.tr("Selection has not done!"))

    def exportFileDialog(self):
        file = QFileDialog.getSaveFileName(self, self.tr("Domestic File"), Settings.value("FileDialog/path") or "", self.tr("Domestic file (*.dfx)"))
        if not file[0] == "":
            db = ReaderDb()
            db.execute("select feed_url from folders where type='feed'")
            allFeed = db.cursor.fetchall()
            root = cElementTree.Element("domestic")
            for feed in allFeed:
                child = cElementTree.SubElement(root, "feed")
                child.text = feed["feed_url"]

            fileW = QFile(file[0])
            fileW.open(QIODevice.WriteOnly|QIODevice.Text)
            fileW.write(cElementTree.tostring(root, "unicode"))
            fileW.close()
            Settings.setValue("FileDialog/path", os.dirname(file[0]))
            Settings.sync()

    def importFileDialog(self):
        file = QFileDialog.getOpenFileName(self, self.tr("Domestic File"), Settings.value("FileDialog/path") or "", self.tr("Domestic file (*.dfx)"))
        if not file[0] == "":
            progressDialog = ProgressDialog(self)
            progressDialog.addFile(file[0])
            progressDialog.show()
            progressDialog.start()

        Settings.setValue("FileDialog/path", os.dirname(file[0]))
        Settings.sync()

    def infoDialog(self):
        items = self.treeWidget.selectedItems()
        if items:
            if isinstance(items[0], FeedItem):
                info = InfoDialog(self)
                info.addItem(items[0])
                info.show()
        else:
            pass

    def aboutDialog(self):
        about = About(self)
        about.show()

    def feedAdd(self):
        f = FeedAddDialog(self)
        f.feedAddFinished.connect(self.feedUpdate)
        f.show()

    def feedFolderAdd(self):
        f = FolderDialog(self)
        f.folderAddFinished.connect(self.sync)
        f.show()

def main():
    app = QApplication(sys.argv)
    LOCALE = QLocale.system().name()
    translator = QTranslator()
    translator.load(os.join(mainPath, "languages", "{}.qm".format(LOCALE)))
    app.installTranslator(translator)
    app.setApplicationName(app.tr("Domestic Reader"))
    app.setApplicationVersion("0.1.8.0")

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
