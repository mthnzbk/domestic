from PyQt5.QtWidgets import QTreeWidgetItem


class AllFeedItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        super(QTreeWidgetItem, self).__init__(parent)
