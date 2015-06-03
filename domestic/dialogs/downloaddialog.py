from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QListWidget, QProgressBar, QListWidgetItem, QWidget
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QUrl, Qt, QFile, QIODevice, QFileInfo, QDir
from domestic.core.settings import Settings
import os.path as os

class CustomListItem(QWidget):
    def __init__(self, parent=None):
        super(CustomListItem, self).__init__(parent)
        self.iconLabel = QLabel()
        pixmap = QPixmap(":/images/icons/audio.png")
        self.iconLabel.setPixmap(pixmap)
        self.nameLabel = QLabel()
        self.nameLabel.setStyleSheet("font-size:17px; font-weight:bold")
        self.statusLabel = QLabel()
        self.statusLabel.setStyleSheet("font-size:14px; color:green")
        self.progressBar = QProgressBar()
        self.progressBar.setFormat("%%p")

        self.vLayout = QVBoxLayout()
        self.hLayout = QHBoxLayout()

        self.vLayout.addWidget(self.nameLabel)

        self.hLayout2 = QHBoxLayout()
        self.hLayout2.addWidget(self.statusLabel)
        self.hLayout2.addWidget(self.progressBar)

        self.vLayout.addLayout(self.hLayout2)

        self.hLayout.addWidget(self.iconLabel, 0)
        self.hLayout.addLayout(self.vLayout, 1)

        self.setLayout(self.hLayout)

        self.manager = QNetworkAccessManager(self)

    def startDownload(self, qurl):
        self.url = qurl
        fileInfo = QFileInfo(qurl.path())
        fileName = fileInfo.fileName()
        filePath = os.join(QDir.homePath(), fileName)

        if QFile.exists(filePath):
            QFile.remove(filePath)

        self.audioFile = QFile(filePath)
        self.audioFile.open(QIODevice.WriteOnly)

        self.nameLabel.setText(fileName)
        self.statusLabel.setText("İndiriliyor...")

        self.request = QNetworkRequest(qurl)
        self.request.setRawHeader("User-Agent", "Domestic Browser 1.0")

        self.reply = self.manager.get(self.request)
        self.reply.downloadProgress.connect(self.setProgress)
        self.reply.readyRead.connect(self.fileReadyRead)
        self.reply.finished.connect(self.finishDownload)

    def fileReadyRead(self):
        self.audioFile.write(self.reply.readAll())

    def setProgress(self, value, max):
        self.progressBar.setMaximum(max)
        self.progressBar.setValue(value)

    def finishDownload(self):
        redirectionTarget = self.reply.attribute(QNetworkRequest.RedirectionTargetAttribute)

        if redirectionTarget is not None:
            newUrl = self.url.resolved(redirectionTarget)
            self.reply.deleteLater()
            self.audioFile.open(QIODevice.WriteOnly)
            self.audioFile.resize(0)
            self.startDownload(newUrl)
            return
        else:
            self.audioFile.flush()
            self.audioFile.close()
            self.statusLabel.setText("İndirildi.")

class DownloaderDialog(QDialog):
    def __init__(self, parent=None):
        super(DownloaderDialog, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle(self.tr("Domestic Downloader"))
        self.listWidget = QListWidget(self)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.listWidget)
        self.setLayout(self.layout)
        self.setFixedSize(600, 350)

    def addUrl(self, url):
        item = QListWidgetItem()
        customItem = CustomListItem()
        item.setSizeHint(customItem.sizeHint())

        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, customItem)

        customItem.startDownload(url)

    def closeEvent(self, event):
        self.hide()