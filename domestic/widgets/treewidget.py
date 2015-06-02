from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QBrush, QColor, QFont
from domestic.core import ReaderDb, Settings
from domestic.widgets.treeitem import FolderItem, FeedItem


class TreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super(QTreeWidget, self).__init__(parent)
        self.parent = parent
        self.setAlternatingRowColors(True)
        self.setIconSize(QSize(18, 18))
        font = QFont()
        font.setBold(True)
        self.setFont(font)
        self.setAnimated(True)
        self.header().setVisible(False)
        self.headerItem().setText(0,"Feed")
        self.itemExpanded.connect(self.expandSignal)
        self.itemCollapsed.connect(self.collapseSignal)

        self.widgetInitial()

        self.itemClicked.connect(self.folderClick)
        self.categorySorting(treeitem=self)
        self.unreadFolderInit()
        self.deletedFolderInit()
        self.storeFolderInit()

        self.parent.syncSignal.connect(self.unreadFolderClick)
        self.parent.syncSignal.connect(self.deletedFolderClick)
        self.parent.syncSignal.connect(self.storeFolderClick)
        self.parent.syncSignal.connect(self.titleSignal)

    def titleSignal(self):
        if not self.currentItem() is None:
            self.treeWidgetTitleSignal.emit(self.currentItem().text(0))

    def collapseSignal(self, item):
        key = "TreeWidget/{}".format(item.title.replace(" ", "-"))
        Settings.setValue(key, 0)
        Settings.sync()

    def expandSignal(self, item):
        key = "TreeWidget/{}".format(item.title.replace(" ", "-"))
        Settings.setValue(key, 1)
        Settings.sync()

    def widgetInitial(self):
        self.unreadFolder = QTreeWidgetItem(self)
        self.unreadFolder.type = "static"
        self.unreadFolder.setIcon(0, QIcon(":/images/icons/folder_home.png"))
        self.unreadFolder.setText(0, self.tr("Unread"))
        self.storeFolder = QTreeWidgetItem(self)
        self.storeFolder.type = "static"
        self.storeFolder.setIcon(0, QIcon(":/images/icons/folder_tar.png"))
        self.storeFolder.setText(0, self.tr("Stored"))
        self.deletedFolder = QTreeWidgetItem(self)
        self.deletedFolder.type = "static"
        self.deletedFolder.setIcon(0, QIcon(":/images/icons/trash_empty.png"))
        self.deletedFolder.setText(0, self.tr("Deleted"))

    categoryList = []
    def categorySorting(self, id=0, treeitem=None):
        db = ReaderDb()
        db.execute("select * from folders where parent=?",(id,))
        folders = db.cursor.fetchall()
        for folder in folders:
            if folder["type"] == "folder":
                item = FolderItem(treeitem)
                item.addOptions(folder)
                self.parent.syncSignal.connect(item.folderClick)
                key = "TreeWidget/{}".format(item.title.replace(" ", "-"))
                if Settings.value(key) != None:
                    item.setExpanded(int(Settings.value(key)))
                self.categoryList.append(item)
                self.categorySorting(folder["id"], item)

            elif folder["type"] == "feed":
                item = FeedItem(treeitem)
                item.addOptions(folder)
                self.parent.syncSignal.connect(item.feedClick)
                self.categoryList.append(item)
                self.categorySorting(folder["id"], item)

    treeWidgetTitleSignal = pyqtSignal(str)
    folderClicked = pyqtSignal(list)
    def folderClick(self, widget, row):
        self.parent.toolBox.widget(0).treeWidget.clear()
        self.parent.toolBox.setCurrentIndex(0)
        if widget == self.unreadFolder:
            self.folderClicked.emit(self.unreadFolderInit())
            self.unreadFolderClick()
        elif widget == self.deletedFolder:
            self.folderClicked.emit(self.deletedFolderInit())
            self.deletedFolderClick()
        elif widget == self.storeFolder:
            self.folderClicked.emit(self.storeFolderInit())
            self.storeFolderClick()
        elif widget.type == "feed":
            self.folderClicked.emit(widget.feedInit())
            widget.feedClick()
        elif widget.type == "folder":
            self.folderClicked.emit(widget.folderInit())
            widget.folderClick()
        self.parent.syncSignal.emit()
        self.treeWidgetTitleSignal.emit(widget.text(0))

    def unreadFolderInit(self):
        db = ReaderDb()
        data = db.execute("select * from store where iscache=1")
        feedList = data.fetchall()
        db.close()
        self.unreadFolder.setForeground(0,QBrush(QColor(0,0,0,255)))
        if len(feedList) > 0:
            self.unreadFolder.setText(0, self.tr("({}) Unread").format(len(feedList)))
            self.unreadFolder.setForeground(0,QBrush(QColor(0,0,255)))
        return feedList

    def unreadFolderClick(self):
        feedList = self.unreadFolderInit()
        if len(feedList) > 0:
            self.unreadFolder.setText(0, self.tr("({}) Unread").format(len(feedList)))
        else: self.unreadFolder.setText(0, self.tr("Unread"))

    def deletedFolderInit(self):
        db = ReaderDb()
        data = db.execute("select * from store where istrash=1")
        feedList = data.fetchall()
        db.close()
        self.deletedFolder.setForeground(0,QBrush(QColor(0,0,0,255)))
        if len(feedList) > 0:
            self.deletedFolder.setText(0, self.tr("({}) Deleted").format(len(feedList)))
            self.deletedFolder.setForeground(0,QBrush(QColor(0,0,255)))
            self.deletedFolder.setIcon(0, QIcon(":/images/icons/trash_full.png"))
        return feedList

    def deletedFolderClick(self):
        feedList = self.deletedFolderInit()
        if len(feedList) > 0:
            self.deletedFolder.setText(0, self.tr("({}) Deleted").format(len(feedList)))
        else: self.deletedFolder.setText(0, self.tr("Deleted"))

    def storeFolderInit(self):
        db = ReaderDb()
        data = db.execute("select * from store where isstore=1")
        feedList = data.fetchall()
        db.close()
        self.storeFolder.setForeground(0,QBrush(QColor(0,0,0,255)))
        if len(feedList) > 0:
            self.storeFolder.setText(0, self.tr("({}) Stored").format(len(feedList)))
            self.storeFolder.setForeground(0,QBrush(QColor(0,0,255)))
        self.treeWidgetTitleSignal.emit(self.storeFolder.text(0))
        return feedList

    def storeFolderClick(self):
        feedList = self.storeFolderInit()
        if len(feedList) > 0:
            self.storeFolder.setText(0, self.tr("({}) Stored").format(len(feedList)))
        else: self.storeFolder.setText(0, self.tr("Stored"))