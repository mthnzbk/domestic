from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

class LastPage(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.textBrowser = QWebView(self)
        self.textBrowser.linkClicked.connect(self.linkClick)
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

    def addTextBrowser(self, data):
        self.textBrowser.setHtml(data)

    def linkClick(self, url):
        print(url)
        QDesktopServices.openUrl(QUrl(url))