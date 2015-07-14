from xml.etree import cElementTree
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QFrame, QProgressBar
from PyQt5.QtCore import QThread, QFile, QIODevice, pyqtSignal, Qt
from domestic.core import ReaderDb, feedInfo
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin


class Thread(QThread):
    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)
        self.parent = parent

    def addFile(self, file):
        self.file = file

    def faviconUrl(self, url):
        try:
            with urlopen(url) as html:
                html = BeautifulSoup(html.read())

                if not html.find(rel="shortcut icon") is None:
                    favicon_url = html.find(rel="shortcut icon")["href"]
                elif not html.find(rel="icon")["href"] is None:
                    favicon_url = html.find(rel="icon")["href"]
                return urljoin(url, favicon_url)
        except:
            return None

    def getFavicon(self, url):
        import sqlite3 as sql
        if not url is None:
            with urlopen(url) as favicon:
                return sql.Binary(favicon.read())
        else: return None

    progress = pyqtSignal(int)
    def run(self):
        if not self.file == "":
            fileR = QFile(self.file)
            fileR.open(QIODevice.ReadOnly|QIODevice.Text)
            etree = cElementTree.XML(fileR.readAll())
            feedList = etree.findall("feed")
            self.parent.progressBar.setMaximum(len(feedList))
            db = ReaderDb()
            counter = 0
            for feed in feedList:
                counter += 1
                self.progress.emit(counter)
                db.execute("select * from folders where feed_url=?", (feed.text,))
                if not db.cursor.fetchone():
                    try:
                        self.parent.labelFeed.setStyleSheet("color:green; font-weight:bold;")
                        self.parent.labelFeed.setText(self.tr("{} adding...").format(feed.text))
                        fInfo = feedInfo(feed.text)
                        fav = self.faviconUrl(fInfo["sitelink"])
                        db.execute("insert into folders (title, type, feed_url, site_url, description, favicon) values (?, 'feed', ?, ?, ?, ?)",
                        (fInfo["title"], fInfo["feedlink"], fInfo["sitelink"], fInfo["description"], self.getFavicon(fav)))
                        db.commit()
                        self.msleep(100)
                    except AttributeError:
                        self.parent.labelFeed.setStyleSheet("color:red; font-weight:bold;")
                        self.parent.labelFeed.setText(self.tr("{} unable to add.").format(feed.text))
                        self.msleep(500)
                else:
                    self.parent.labelFeed.setStyleSheet("color:blue; font-weight:bold;")
                    self.parent.labelFeed.setText(self.tr("{} added.").format(feed.text))
                    self.msleep(500)
            db.close()
            fileR.close()


class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super(ProgressDialog, self).__init__(parent)
        self.parent = parent
        self.resize(400, 175)
        self.setMaximumSize(450, 200)
        self.verticalLayout = QVBoxLayout(self)
        self.labelInfo = QLabel(self)
        self.verticalLayout.addWidget(self.labelInfo)
        self.labelFeed = QLabel(self)
        self.verticalLayout.addWidget(self.labelFeed)
        self.progressBar = QProgressBar(self)
        self.progressBar.setFormat("%v/%m")
        self.verticalLayout.addWidget(self.progressBar)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)

        self.setWindowTitle(self.tr("Importing Feeds..."))
        self.labelInfo.setText(self.tr("<span style='font-size:11pt; font-weight:bold;'>Imported:</span>"))

        self.thread = Thread(self)
        self.thread.progress.connect(self.progressBar.setValue)


    def keyPressEvent(self, event):
        pass

    def accept(self):
        self.parent.syncSignal.emit()
        self.parent.categorySync()
        self.close()

    def finish(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        self.buttonBox.button(QDialogButtonBox.Ok).setFocus()

    def addFile(self, file):
        self.file = file

    def getFile(self):
        return self.file

    def start(self):
        self.thread.addFile(self.getFile())
        self.thread.start()
        self.thread.finished.connect(self.finish)