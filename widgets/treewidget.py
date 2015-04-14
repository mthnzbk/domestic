from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from core import ReaderDb, readAllFeedEntries

class TreeWidget(QTreeWidget):
    unreadFolderSignal = pyqtSignal(list)
    deletedFolderSignal = pyqtSignal(list)
    storeFolderSignal = pyqtSignal(list)
    def __init__(self, parent=None):
        super(QTreeWidget, self).__init__(parent)
        self.parent = parent
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setAlternatingRowColors(True)
        self.setIconSize(QSize(12, 12))
        self.setAnimated(True)
        self.header().setVisible(False)
        self.headerItem().setText(0,"Feed")
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.unreadFolder = QTreeWidgetItem(self)
        #self.unreadFolder.setDisabled(True)
        self.unreadFolder.setText(0, "Okunmamışlar")
        self.deletedFolder = QTreeWidgetItem(self)
        self.deletedFolder.setText(0, "Silinenler")
        self.storeFolder = QTreeWidgetItem(self)
        self.storeFolder.setText(0, "Saklananlar")
        self.allFeedFolder = QTreeWidgetItem(self)
        self.allFeedFolder.setText(0, "Tüm Beslemeler")
        self.itemClicked.connect(self.folderClick)

        self.setCurrentItem(self.unreadFolder) # başlangıçta seçili olanı yüklemesi sağlanacak.
        self.unreadTitleSignal.emit(self.unreadFolder.text(0))

        db = ReaderDb()
        allFeed = db.allFeed()
        for url, title in allFeed:
            item = QTreeWidgetItem(self.allFeedFolder)
            item.setText(0, title)
            item.url = url



    def folderClick(self, widget, row):
        print(widget, row)
        if widget == self.unreadFolder:
            self.parent.widget(1).setCurrentIndex(0)
            self.unreadFolderClick()
        elif widget == self.deletedFolder:
            self.parent.widget(1).setCurrentIndex(0)
            self.deletedFolderClick()
        elif widget == self.storeFolder:
            self.parent.widget(1).setCurrentIndex(0)
            self.storeFolderClick()
        elif widget == self.allFeedFolder:
            self.allFeedFolderClick()
        else: pass

    unreadTitleSignal = pyqtSignal(str)
    def unreadFolderClick(self):
        if not self.unreadFolder.isDisabled():
            db = ReaderDb()
            feedList = db.feedsList()
            #e = readAllFeedEntries(feedList)
            self.unreadTitleSignal.emit(self.unreadFolder.text(0))
            self.unreadFolderSignal.emit(feedList)
        else:pass

    deletedTitleSignal = pyqtSignal(str)
    def deletedFolderClick(self):
        db = ReaderDb()
        feedList = db.deletedFeeds()
        self.deletedTitleSignal.emit(self.deletedFolder.text(0))
        self.deletedFolderSignal.emit(feedList)

    storeTitleSignal = pyqtSignal(str)
    def storeFolderClick(self):
        db = ReaderDb()
        feedList = db.storeFeeds()
        self.storeFolderSignal.emit(feedList)
        self.storeTitleSignal.emit(self.storeFolder.text(0))

    allFeedTitleSignal = pyqtSignal(str)
    def allFeedFolderClick(self):
        self.allFeedTitleSignal.emit(self.allFeedFolder.text(0))
        if self.allFeedFolder.isExpanded():
            self.allFeedFolder.setExpanded(False)
        else:
            self.allFeedFolder.setExpanded(True)