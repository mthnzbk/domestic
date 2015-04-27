from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

from core.settings import Settings


class LastPage(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.Layout = QVBoxLayout(self)
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.browser = QWebView(self)
        self.browser.resize(Settings.value("ToolWebView/size"))
        #self.browser.linkClicked.connect(self.linkClick)
        self.infoLabel = QLabel(self)
        self.Layout.addWidget(self.infoLabel)
        self.Layout.addWidget(self.browser)

    def addHtml(self, data):
        self.browser.setHtml(data)

    def linkClick(self, url): # FIXME
        print(url)
        QDesktopServices.openUrl(QUrl(url))