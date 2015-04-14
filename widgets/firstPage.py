from PyQt5.QtWidgets import QWidget, QGridLayout, QTreeWidgetItem, QTreeWidget, QHeaderView
from widgets.settings import Settings


class FirstPage(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.treeWidget = QTreeWidget(self)
        self.treeWidget.setColumnCount(5)
        self.treeWidget.header().ResizeMode(QHeaderView.ResizeToContents)
        self.treeWidget.header().resizeSection(0, int(Settings.value("TreeWidgetHeader/size0")))
        self.treeWidget.header().resizeSection(1, int(Settings.value("TreeWidgetHeader/size1")))
        self.treeWidget.header().resizeSection(2, int(Settings.value("TreeWidgetHeader/size2")))
        self.treeWidget.header().resizeSection(3, int(Settings.value("TreeWidgetHeader/size3")))
        self.treeWidget.header().resizeSection(4, int(Settings.value("TreeWidgetHeader/size4")))
        self.gridLayout.addWidget(self.treeWidget, 0, 0, 1, 1)

        self.treeWidget.itemClicked.connect(self.feedClick)

        self.treeWidget.headerItem().setText(0, "Site")
        self.treeWidget.headerItem().setText(1, "Başlık")
        self.treeWidget.headerItem().setText(2, "Yazar")
        self.treeWidget.headerItem().setText(3, "Kategori")
        self.treeWidget.headerItem().setText(4, "Tarih")


    def feedClick(self, a, b):
        self.parent.setCurrentIndex(1)
        w = self.parent.currentWidget()
        w.addTextBrowser(a.content)

    def feedList(self, l=None):
        if len(l):
            print(l)
            for i in l:
                item = QTreeWidgetItem(self.treeWidget)
                item.setText(0, i[0])
                item.setText(1, i[1])
                item.setText(2, i[2])
                item.setText(3, i[3])
                item.setText(4, i[4])
                item.content = i[6]
        else:
            self.treeWidget.clear()
