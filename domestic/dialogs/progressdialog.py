from xml.etree import cElementTree
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QFrame, QProgressBar
from PyQt5.QtCore import QThread, QFile, QIODevice, pyqtSignal, Qt
from domestic.core import ReaderDb, feedInfo


class Thread(QThread):
    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)
        self.parent = parent

    def addFile(self, file):
        self.file = file

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
                        self.parent.labelFeed.setText("{} adding.".format(feed.text))
                        fInfo = feedInfo(feed.text)
                        db.execute("insert into folders (title, type, feed_url, site_url, description) values (?, 'feed', ?, ?, ?)",
                        (fInfo["title"], fInfo["feedlink"], fInfo["sitelink"], fInfo["description"]))
                        db.commit()
                        self.msleep(100)
                    except AttributeError:
                        self.parent.labelFeed.setStyleSheet("color:red; font-weight:bold;")
                        self.parent.labelFeed.setText("{} unable to add.".format(feed.text))
                        self.msleep(500)
                else:
                    self.parent.labelFeed.setStyleSheet("color:blue; font-weight:bold;")
                    self.parent.labelFeed.setText("{} added.".format(feed.text))
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
        self.parent.sync()
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