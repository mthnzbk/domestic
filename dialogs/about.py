from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QGridLayout, QLabel, QTextBrowser, QDialogButtonBox
from PyQt5.QtWidgets import QApplication as app

class About(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.setMinimumSize(600, 480)
        self.setMaximumSize(600,480)
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

        self.tabDonate = QWidget()
        self.gridLayout4 = QGridLayout(self.tabDonate)
        self.viewDonate = QTextBrowser(self.tabDonate)
        self.gridLayout4.addWidget(self.viewDonate, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabDonate, "")

        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)
        self.buttonBox.button(QDialogButtonBox.Close).setText("Kapat")
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.reject)

        self.setWindowTitle("Hakkında")
        self.labelAbout.setText("TextLabel")

        import os.path as os
        with open(os.join(os.dirname(os.dirname(__file__)), "LICENSE"),"r") as license:
            self.browserLicense.setText(license.read())

        self.viewDonate.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabVersion), "Sürüm Bilgileri")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLicense), "Lisans")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDonate), "Bağış Yapın")
        self.labelAbout.setText("""
        <p align="center"><img src=":/images/rss-icon-128.png"/></p>
        <p align="center"><span style=" font-size:20pt; font-weight:bold;">{}</span></p>
        <p align="center">Sürüm: {}</p><p align="center"></p>
        <p>Domestic RSS Reader, çapraz platformlu, özgür ve ücretsiz bir</p>
        <p>RSS/Atom besleme okuyucusudur.</p>
        <p>PyQt5(Qt5), Python3.4 ve sqlite3 ile oluşturulmuştur.</p>
        <p>Lisans: Gpl v3</p>
        <p align="center">Copyright © 2015 Metehan Özbek - <a href="http://metehan.us">
            <span style=" color:#0000ff;">metehan.us</span></a></p>
                                """.format(app.applicationName(), app.applicationVersion()))

