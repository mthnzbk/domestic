from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSlider
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtNetwork import QNetworkRequest
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, Qt, pyqtSignal
from domestic.core.settings import Settings
import time

class PodCastPlayer(QWidget):

    downloadClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.playButton = QPushButton(self)
        self.playButton.setText(self.tr("Play"))
        self.pauseButton = QPushButton(self)
        self.pauseButton.setText(self.tr("Pause"))
        self.stopButton = QPushButton(self)
        self.stopButton.setText(self.tr("Stop"))
        self.playerProgress = QSlider(self)
        self.playerProgress.setOrientation(Qt.Horizontal)
        self.playerProgress.setValue(0)
        self.timeLabel = QLabel(self)
        self.timeLabel.setText("00:00")
        self.durationLabel = QLabel(self)
        self.durationLabel.setText("00:00")

        self.downloadButton = QPushButton(self)
        self.downloadButton.setText(self.tr("Download"))

        self.layout.addWidget(self.playButton)
        self.layout.addWidget(self.pauseButton)
        self.layout.addWidget(self.stopButton)
        self.layout.addWidget(self.timeLabel)
        self.layout.addWidget(self.playerProgress)
        self.layout.addWidget(self.durationLabel)
        self.layout.addWidget(self.downloadButton)

        self.mediaPlayer = QMediaPlayer(self)
        self.mediaPlayer.setVolume(100)

        self.playButton.clicked.connect(self.play)
        self.pauseButton.clicked.connect(self.pause)
        self.stopButton.clicked.connect(self.stop)
        self.downloadButton.clicked.connect(self.downloadClicked)

        self.playerProgress.sliderMoved.connect(self.mediaPlayer.setPosition)

        self.mediaPlayer.durationChanged.connect(self.playerProgress.setMaximum)
        self.mediaPlayer.durationChanged.connect(self.setDurationLabel)
        self.mediaPlayer.positionChanged.connect(self.setTimeLabel)
        self.mediaPlayer.positionChanged.connect(self.playerProgress.setValue)

    def setDurationLabel(self, duration):
        self.durationLabel.setText(time.strftime("%H:%M:%S", time.gmtime(duration/1000)))

    def setTimeLabel(self, pos):
        self.timeLabel.setText(time.strftime("%H:%M:%S", time.gmtime(pos/1000)))

    def addMedia(self, media):
        self.url = QUrl(media)
        self.playerProgress.setValue(0)
        self.timeLabel.setText("00:00")
        self.durationLabel.setText("00:00")
        self.mediaPlayer.setMedia(QMediaContent(QNetworkRequest(self.url)))

    def play(self):
        self.mediaPlayer.play()

    def pause(self):
        self.mediaPlayer.pause()

    def stop(self):
        self.mediaPlayer.stop()

class LastPage(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.browser = QWebView(self)
        self.browser.resize(Settings.value("ToolWebView/size"))
        self.infoLabel = QLabel(self)
        self.infoLabel.linkActivated.connect(self.linkClick)
        self.player = PodCastPlayer(self)
        self.player.hide()

        self.layout.addWidget(self.infoLabel)
        self.layout.addWidget(self.player)
        self.layout.addWidget(self.browser)

        self.player.downloadClicked.connect(self.downloadPodcast)

    def downloadPodcast(self):
        self.parent.downloadDialog.addUrl(self.player.url)

    def insertEntry(self, item):
        self.infoLabel.setText(self.tr("""<p><a style='font-size:13pt; font-weight:bold' href='{}'>{}</a> - <span>Date: {}</span></p>
        <p>Author: {} | Category: {}</p>""").format(item.getEntryUrl(), item.getEntryTitle(), item.getEntryDateTime(),
            item.getEntryAuthor(), item.getEntryCategory()))
        self.browser.setHtml(item.getEntryContent())
        if not item.getEnclosureUrl() is None:
            self.player.show()
            self.player.addMedia(item.getEnclosureUrl())
        else:
            self.player.hide()

    def linkClick(self, url):
        QDesktopServices.openUrl(QUrl(url))