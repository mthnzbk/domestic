from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from core import ReaderDb, readAllFeedEntries

class TreeWidget(QTreeWidget):
    unreadFolderSignal = pyqtSignal(list)
    deletedFolderSignal = pyqtSignal(list)
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
        self.unreadFolder.setText(0, "Okunmamışlar")
        self.deletedFolder = QTreeWidgetItem(self)
        self.deletedFolder.setText(0, "Silinenler")
        self.storeFolder = QTreeWidgetItem(self)
        self.storeFolder.setText(0, "Saklananlar")
        self.allFeedFolder = QTreeWidgetItem(self)
        self.allFeedFolder.setText(0, "Tüm Beslemeler")
        self.itemClicked.connect(self.folderClick)



    def folderClick(self, widget, row):
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

    def unreadFolderClick(self):
        db = ReaderDb()
        feedList = db.feedListDb()
        e = readAllFeedEntries(feedList)
        self.unreadFolderSignal.emit(e)

    def deletedFolderClick(self):
        db = ReaderDb()
        feedList = db.deletedFeeds()
        self.deletedFolderSignal.emit(feedList)


    def storeFolderClick(self):
        print("3")
        pass

    def allFeedFolderClick(self):
        print("4")
        pass