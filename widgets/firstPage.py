from PyQt5.QtWidgets import QWidget, QGridLayout, QTreeWidgetItem, QTreeWidget

class FirstPage(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.treeWidget = QTreeWidget(self)

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
            for i in l:
                item = QTreeWidgetItem(self.treeWidget)
                item.setText(0, i[0])
                item.setText(1, i[1])
                item.setText(2, i[2])
                item.setText(3, i[3])
                item.setText(4, i[5])
                item.content = i[6]
        else:
            self.treeWidget.clear()
