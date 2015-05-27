from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QGridLayout, QLabel, QTextBrowser, QDialogButtonBox
from PyQt5.QtWidgets import QApplication as app
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

class About(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.setMinimumSize(600, 500)
        self.setMaximumSize(600, 500)
        self.verticalLayout = QVBoxLayout(self)
        self.tabWidget = QTabWidget(self)
        self.tabVersion = QWidget()
        self.gridLayout3 = QGridLayout(self.tabVersion)
        self.labelAbout = QLabel(self.tabVersion)
        self.gridLayout3.addWidget(self.labelAbout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabVersion, "")

        self.tabLicense = QWidget()
        self.gridLayout2 = QGridLayout(self.tabLicense)
        self.browserLicense = QTextBrowser(self.tabLicense)
        self.gridLayout2.addWidget(self.browserLicense, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabLicense, "")

        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)
        self.buttonBox.button(QDialogButtonBox.Close).setText(self.tr("Close"))
        self.buttonBox.button(QDialogButtonBox.Close).clicked.connect(self.reject)
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.reject)
        self.setWindowTitle(self.tr("About"))

        import os.path as os
        with open(os.join(os.dirname(os.dirname(__file__)), "LICENSE"),"r") as license:
            self.browserLicense.setText(license.read())

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabVersion), self.tr("Version"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLicense), self.tr("License"))
        self.labelAbout.setText(self.tr("""
        <p align="center"><img src=":/images/rss-icon-128.png"/></p>
        <p align="center"><span style=" font-size:20pt; font-weight:bold;">{0}</span></p>
        <p align="center">Version: {1}</p><p align="center"></p>
        <p>{0}, cross platform, free and free is a RSS/Atom reader.</p>
        <p>PyQt5(Qt5), Python3.4, BeautifulSoup4, feedparser and sqlite3 was created with.</p>
        <p>License: Gpl v3</p>
        <p align="center">Copyright \u00a9 2015 Metehan Özbek - <a href="http://metehan.us">
            <span style=" color:#0000ff;">metehan.us </span></a> - <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=M9BAR7J2SQWZC">
          <img src=":/images/donate-button.png" /></a></p>""").format(app.applicationName(), app.applicationVersion()))

        self.labelAbout.linkActivated.connect(self.openUrl)

    def openUrl(self, url):
        QDesktopServices.openUrl(QUrl(url))

