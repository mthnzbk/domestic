from PyQt5.QtWidgets import QWidget, QGridLayout, QTreeWidgetItem, QTreeWidget

class FirstPage(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.treeWidget = QTreeWidget(self)
        item_0 = QTreeWidgetItem(self.treeWidget)
        self.gridLayout.addWidget(self.treeWidget, 0, 0, 1, 1)

        self.treeWidget.clicked['QModelIndex'].connect(self.close)

        self.treeWidget.headerItem().setText(0, "Site")
        self.treeWidget.headerItem().setText(1, "Başlık")
        self.treeWidget.headerItem().setText(2, "Yazar")
        self.treeWidget.headerItem().setText(3, "Kategori")
        self.treeWidget.headerItem().setText(4, "Tarih")

        self.treeWidget.topLevelItem(0).setText(0, "MetehanUs")
        self.treeWidget.topLevelItem(0).setText(1, "Pygame Time Modülü")
        self.treeWidget.topLevelItem(0).setText(2, "Özbek Metehan")
        self.treeWidget.topLevelItem(0).setText(3, "Python, pygame")
        self.treeWidget.topLevelItem(0).setText(4, "25.06.1990")