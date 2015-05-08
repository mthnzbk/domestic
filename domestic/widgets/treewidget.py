from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QBrush, QColor, QFont, QPixmap
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

    def collapseSignal(self, item):
        key = "TreeWidget/{}".format(item.text(0).replace(" ", "-"))
        Settings.setValue(key, 0)
        Settings.sync()

    def expandSignal(self, item):
        key = "TreeWidget/{}".format(item.text(0).replace(" ", "-"))
        Settings.setValue(key, 1)
        Settings.sync()

    def widgetInitial(self):
        self.unreadFolder = QTreeWidgetItem(self)
        self.unreadFolder.setIcon(0, QIcon(":/images/icons/folder_home.png"))
        self.unreadFolder.setText(0, self.tr("Unread"))
        self.deletedFolder = QTreeWidgetItem(self)
        self.deletedFolder.setIcon(0, QIcon(":/images/icons/trash_empty.png"))
        self.deletedFolder.setText(0, self.tr("Deleted"))
        self.storeFolder = QTreeWidgetItem(self)
        self.storeFolder.setIcon(0, QIcon(":/images/icons/folder_tar.png"))
        self.storeFolder.setText(0, self.tr("Stored"))

    def categorySorting(self, id=0, treeitem=None):
        db = ReaderDb()
        db.execute("select * from folders where parent=?",(id,))
        folders = db.cursor.fetchall()
        for folder in folders:
            if folder["type"] == "folder":
                item = FolderItem(treeitem)
                item.setIcon(0, QIcon(":/images/icons/folder_grey.png"))
                item.id = folder["id"]
                item.title = folder["title"]
                item.type = folder["type"]
                item.setText(0, item.title)
                item.parent = folder["parent"]
                key = "TreeWidget/{}".format(item.text(0).replace(" ", "-"))
                if Settings.value(key) != None:
                    item.setExpanded(int(Settings.value(key)))
                self.categorySorting(folder["id"], item)

            elif folder["type"] == "feed":
                item = FeedItem(treeitem)
                item.id = folder["id"]
                item.title = folder["title"]
                item.setText(0, item.title)
                item.parent = folder["parent"]
                item.feed_url = folder["feed_url"]
                item.site_url = folder["site_url"]
                item.type = folder["type"]
                item.description = folder["description"]
                item.favicon = folder["favicon"]
                if not item.favicon is None:
                    icon = QIcon()
                    pix = QPixmap()
                    pix.loadFromData(item.favicon)
                    icon.addPixmap(pix)
                    item.setIcon(0, icon)
                else:
                    item.setIcon(0, QIcon(":/images/icons/html.png"))
                self.categorySorting(folder["id"], item)

    treeWidgetTitleSignal = pyqtSignal(str)
    folderClicked = pyqtSignal()
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
        else:
            self.folderClicked.emit()
        self.treeWidgetTitleSignal.emit(widget.text(0))

    def unreadFolderInit(self):
        db = ReaderDb()
        data = db.execute("select * from store where iscache=1")
        feedList = data.fetchall()
        db.close()
        self.unreadFolder.setForeground(0,QBrush(QColor(0,0,0,255)))
        if len(feedList) > 0:
            self.unreadFolder.setText(0, self.tr("Unread ({})").format(len(feedList)))
            self.unreadFolder.setForeground(0,QBrush(QColor(0,0,255)))
        return feedList

    def deletedFolderInit(self):
        db = ReaderDb()
        data = db.execute("select * from store where istrash=1")
        feedList = data.fetchall()
        db.close()
        self.deletedFolder.setForeground(0,QBrush(QColor(0,0,0,255)))
        if len(feedList) > 0:
            self.deletedFolder.setText(0, self.tr("Deleted ({})").format(len(feedList)))
            self.deletedFolder.setForeground(0,QBrush(QColor(0,0,255)))
            self.deletedFolder.setIcon(0, QIcon(":/images/icons/trash_full.png"))
        return feedList

    def storeFolderInit(self):
        db = ReaderDb()
        data = db.execute("select * from store where isstore=1")
        feedList = data.fetchall()
        db.close()
        self.storeFolder.setForeground(0,QBrush(QColor(0,0,0,255)))
        if len(feedList) > 0:
            self.storeFolder.setText(0, self.tr("Stored ({})").format(len(feedList)))
            self.storeFolder.setForeground(0,QBrush(QColor(0,0,255)))
        return feedList

    unreadFolderClicked = pyqtSignal(list)
    def unreadFolderClick(self):
        self.parent.widget(1).widget(0).treeWidget.clear()
        if not self.unreadFolder.isDisabled():
            feedList = self.unreadFolderInit()
            self.unreadFolderClicked.emit(feedList)
            if len(feedList) > 0:
                self.unreadFolder.setText(0, self.tr("Unread ({})").format(len(feedList)))
            else: self.unreadFolder.setText(0, self.tr("Unread"))
            self.treeWidgetTitleSignal.emit(self.unreadFolder.text(0))

    deletedFolderClicked = pyqtSignal(list)
    def deletedFolderClick(self):
        self.parent.widget(1).widget(0).treeWidget.clear()
        feedList = self.deletedFolderInit()
        self.deletedFolderClicked.emit(feedList)
        if len(feedList) > 0:
            self.deletedFolder.setText(0, self.tr("Deleted ({})").format(len(feedList)))
        else: self.deletedFolder.setText(0, self.tr("Deleted"))
        self.treeWidgetTitleSignal.emit(self.deletedFolder.text(0))

    storeFolderClicked = pyqtSignal(list)
    def storeFolderClick(self):
        self.parent.widget(1).widget(0).treeWidget.clear()
        feedList = self.storeFolderInit()
        self.storeFolderClicked.emit(feedList)
        if len(feedList) > 0:
            self.storeFolder.setText(0, self.tr("Stored ({})").format(len(feedList)))
        else: self.storeFolder.setText(0, self.tr("Stored"))
        self.treeWidgetTitleSignal.emit(self.storeFolder.text(0))