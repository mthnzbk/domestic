from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QBrush, QColor, QFont
from core import ReaderDb
from widgets.treeitem import FolderItem, FeedItem

class TreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super(QTreeWidget, self).__init__(parent)
        self.parent = parent
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setAlternatingRowColors(True)
        self.setIconSize(QSize(24, 24))
        self.setAnimated(True)
        self.header().setVisible(False)
        self.headerItem().setText(0,"Feed")
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.widgetInitial()

        self.itemClicked.connect(self.folderClick)
        #self.unreadTitleSignal.emit(self.unreadFolder.text(0))
        self.categorySorting(treeitem=self.allFeedFolder)
        self.unreadFolderInıt()
        self.deletedFolderInıt()
        self.storeFolderInıt()

    def widgetInitial(self):
        self.unreadFolder = QTreeWidgetItem(self)
        self.unreadFolder.setIcon(0, QIcon(":/images/icons/folder_home.png"))
        self.unreadFolder.setText(0, self.tr("Okunmamışlar"))
        self.deletedFolder = QTreeWidgetItem(self)
        self.deletedFolder.setIcon(0, QIcon(":/images/icons/trash_empty.png"))
        self.deletedFolder.setText(0, self.tr("Silinenler"))
        self.storeFolder = QTreeWidgetItem(self)
        self.storeFolder.setIcon(0, QIcon(":/images/icons/folder_tar.png"))
        self.storeFolder.setText(0, self.tr("Saklananlar"))
        self.allFeedFolder = QTreeWidgetItem(self)
        self.allFeedFolder.setIcon(0, QIcon(":/images/icons/folder_grey_open.png"))
        self.allFeedFolder.setText(0, self.tr("Tüm Beslemeler"))

        self.expandItem(self.allFeedFolder)

    def categorySorting(self, id=0, treeitem=None):
        db = ReaderDb()
        db.execute("select * from categories where subcategory=?",(id,))
        data = db.cursor.fetchall()
        for da in data:
            item = QTreeWidgetItem(treeitem)
            item.setExpanded(True)
            item.setIcon(0, QIcon(":/images/icons/folder_grey.png"))
            item.id = da["id"]
            item.category_name = da[1]
            item.setText(0, item.category_name)
            item.subcategory = da["subcategory"]
            print(da["id"], da["category_name"], da["subcategory"])
            self.categorySorting(da["id"], item)

    treeWidgetTitleSignal = pyqtSignal(str)
    folderClicked = pyqtSignal()
    def folderClick(self, widget, row):
        print(widget, widget.text(0))

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
        else:
            self.folderClicked.emit()
        self.treeWidgetTitleSignal.emit(widget.text(0))

    def unreadFolderInıt(self):
        db = ReaderDb()
        data = db.execute("select * from store where iscache=1")
        feedList = data.fetchall()
        db.close()
        print(len(feedList), feedList)
        #self.unreadFolderClicked.emit(feedList)
        if len(feedList) > 0:
            self.unreadFolder.setText(0, self.tr("Okunmamışlar ({})").format(len(feedList)))
            font = QFont()
            font.setBold(True)
            self.unreadFolder.setFont(0, font)
            self.unreadFolder.setForeground(0,QBrush(QColor(0,0,255)))
            #self.deletedFolder.setIcon(0, QIcon(":/images/icons/trash_full.png"))
        return feedList

    def deletedFolderInıt(self):
        db = ReaderDb()
        data = db.execute("select * from store where istrash=1")
        feedList = data.fetchall()
        db.close()
        print(len(feedList), feedList)
        #self.deletedFolderClicked.emit(feedList)
        if len(feedList) > 0:
                self.deletedFolder.setText(0, self.tr("Silinenler ({})").format(len(feedList)))
        return feedList

    def storeFolderInıt(self):
        db = ReaderDb()
        data = db.execute("select * from store where isstore=1")
        feedList = data.fetchall()
        db.close()
        #self.storeFolderClicked.emit(feedList)
        print(len(feedList), feedList)
        if len(feedList) > 0:
            self.storeFolder.setText(0, self.tr("Saklananlar ({})").format(len(feedList)))
        return feedList

    unreadFolderClicked = pyqtSignal(list)
    def unreadFolderClick(self):
        self.parent.widget(1).widget(0).treeWidget.clear()
        if not self.unreadFolder.isDisabled():
            feedList = self.unreadFolderInıt()
            print(len(feedList), feedList)
            self.unreadFolderClicked.emit(feedList)
            if len(feedList) > 0:
                self.unreadFolder.setText(0, self.tr("Okunmamışlar ({})").format(len(feedList)))
                #self.deletedFolder.setIcon(0, QIcon(":/images/icons/trash_full.png"))
            else: self.unreadFolder.setText(0, self.tr("Okunmamışlar"))
            self.treeWidgetTitleSignal.emit(self.unreadFolder.text(0))

    deletedFolderClicked = pyqtSignal(list)
    def deletedFolderClick(self):
        self.parent.widget(1).widget(0).treeWidget.clear()
        feedList = self.deletedFolderInıt()
        print(len(feedList), feedList)
        self.deletedFolderClicked.emit(feedList)
        if len(feedList) > 0:
            self.deletedFolder.setText(0, self.tr("Silinenler ({})").format(len(feedList)))
        else: self.deletedFolder.setText(0, self.tr("Silinenler"))
        self.treeWidgetTitleSignal.emit(self.deletedFolder.text(0))

    storeFolderClicked = pyqtSignal(list)
    def storeFolderClick(self):
        self.parent.widget(1).widget(0).treeWidget.clear()
        feedList = self.storeFolderInıt()
        self.storeFolderClicked.emit(feedList)
        print(len(feedList), feedList)
        if len(feedList) > 0:
            self.storeFolder.setText(0, self.tr("Saklananlar ({})").format(len(feedList)))
        else: self.storeFolder.setText(0, self.tr("Saklananlar"))
        self.treeWidgetTitleSignal.emit(self.storeFolder.text(0))

    def allFeedFolderClick(self):
        if self.allFeedFolder.isExpanded():
            self.allFeedFolder.setExpanded(False)
            #self.allFeedFolder.setIcon(0, QIcon(":/images/icons/folder_grey.png"))
        else:
            self.allFeedFolder.setExpanded(True)
            #self.allFeedFolder.setIcon(0, QIcon(":/images/icons/folder_grey_open.png"))
