from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QFont

from widgets.treeitem import EntryItem
from core.settings import Settings


class FirstPage(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.parent = parent

        self.Layout = QVBoxLayout(self)
        self.Layout.setContentsMargins(0, 0, 0, 0)

        self.treeWidget = QTreeWidget(self)
        font = QFont()
        font.setBold(True)
        self.treeWidget.setFont(font)
        self.treeWidget.resize(Settings.value("ToolTreeWidget/size"))
        self.treeWidget.setColumnCount(5)
        self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeWidget.header().setSectionsMovable(False)
        self.treeWidget.header().ResizeMode(QHeaderView.ResizeToContents)
        self.treeWidget.header().resizeSection(0, int(Settings.value("TreeWidgetHeader/size0")))
        self.treeWidget.header().resizeSection(1, int(Settings.value("TreeWidgetHeader/size1")))
        self.treeWidget.header().resizeSection(2, int(Settings.value("TreeWidgetHeader/size2")))
        self.treeWidget.header().resizeSection(3, int(Settings.value("TreeWidgetHeader/size3")))
        self.treeWidget.header().resizeSection(4, int(Settings.value("TreeWidgetHeader/size4")))
        self.Layout.addWidget(self.treeWidget)

        self.treeWidget.itemDoubleClicked.connect(self.feedClick)

        self.treeWidget.headerItem().setText(0, self.tr("Site"))
        self.treeWidget.headerItem().setText(1, self.tr("Başlık"))
        self.treeWidget.headerItem().setText(2, self.tr("Yazar"))
        self.treeWidget.headerItem().setText(3, self.tr("Kategori"))
        self.treeWidget.headerItem().setText(4, self.tr("Tarih"))


    def feedClick(self, item, b):
        self.parent.setCurrentIndex(1)
        current = self.parent.currentWidget()
        current.insertEntry(item)

    def entryList(self, entryList=None):
        if len(entryList):
            print(entryList)
            for entry in entryList:
                item = EntryItem(self.treeWidget)
                item.id(entry[0]), item.feedUrl(entry[1]), item.feedTitle(entry[2]), item.entryUrl(entry[3]), item.entryTitle(entry[4])
                item.entryAuthor(entry[5]), item.entryCategory(entry[6]), item.entryDateTime(entry[7]), item.entryContent(entry[8])
                item.isstore, item.istrash, item.iscache = entry[9], entry[10], entry[11]
        else:
            self.treeWidget.clear()
