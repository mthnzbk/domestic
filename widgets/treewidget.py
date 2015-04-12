from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt, QSize
from widgets.menu import FeedMenu

class TreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super(QTreeWidget, self).__init__(parent)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setAlternatingRowColors(True)

        self.setIconSize(QSize(12, 12))
        self.setAnimated(True)
        self.header().setVisible(False)
        self.headerItem().setText(0,"Feed")
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        '''self.actionFeedRefresh = QAction(self)
        #self.actionFeedRefresh.setSeparator(True)
        self.actionFeedRefresh.setText("Besleme güncelle")
        self.actionFeedRefresh.setShortcut("F5")
        self.addAction(self.actionFeedRefresh)

        self.actionRefresh = QAction(self)
        self.actionRefresh.setText("Tümünü güncelle")
        self.actionRefresh.setShortcut("Ctrl+F5")
        self.addAction(self.actionRefresh)

        self.actionDelete = QAction(self)
        self.actionDelete.setText("Sil")
        self.addAction(self.actionDelete)

        self.actionReadMark = QAction(self)
        self.actionReadMark.setText("Okundu/Okunmadı olarak işaretle")
        self.addAction(self.actionReadMark)
        #self.actionReadMark.setSeparator(True)

        self.actionPreference = QAction(self)
        self.actionPreference.setText("Özellikler")
        self.addAction(self.actionPreference)'''


        self.pressed['QModelIndex'].connect(self.expandAll)

        item_0 = QTreeWidgetItem(self)
        item_0 = QTreeWidgetItem(self)
        item_0 = QTreeWidgetItem(self)
        item_0 = QTreeWidgetItem(self)
        item_1 = QTreeWidgetItem(item_0)
        item_1 = QTreeWidgetItem(item_0)
        item_2 = QTreeWidgetItem(item_1)

        self.topLevelItem(0).setText(0, "Okunmamışlar")
        self.topLevelItem(1).setText(0, "Silinenler")
        self.topLevelItem(2).setText(0, "Saklananlar")
        self.topLevelItem(3).setText(0, "Tüm Beslemeler")
        self.topLevelItem(3).child(0).setText(0, "MetehanUs")
        self.topLevelItem(3).child(1).setText(0, "Haberler")
        self.topLevelItem(3).child(1).child(0).setText(0, "Hürriyet")

    def contextMenuEvent(self, event):
        menu = FeedMenu(self)
        menu.exec_()