from PyQt5.QtWidgets import QWidget, QGridLayout, QTextBrowser

class LastPage(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.textBrowser = QTextBrowser(self)
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

    def addTextBrowser(self, data):
        self.textBrowser.setHtml(data)