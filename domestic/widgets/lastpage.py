from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from domestic.core.settings import Settings


class LastPage(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.Layout = QVBoxLayout(self)
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.browser = QWebView(self)
        self.browser.resize(Settings.value("ToolWebView/size"))
        self.infoLabel = QLabel(self)
        self.infoLabel.linkActivated.connect(self.linkClick)
        self.Layout.addWidget(self.infoLabel)
        self.Layout.addWidget(self.browser)

    def insertEntry(self, item):
        self.infoLabel.setText(self.tr("""<p><a style='font-size:13pt; font-weight:bold' href='{}'>{}</a> - <span>Date: {}</span></p>
        <p>Author: {} | Category: {}</p>""").format(item.getEntryUrl(), item.getEntryTitle(), item.getEntryDateTime(),
            item.getEntryAuthor(), item.getEntryCategory()))
        self.browser.setHtml(item.getEntryContent())

    def linkClick(self, url):
        QDesktopServices.openUrl(QUrl(url))