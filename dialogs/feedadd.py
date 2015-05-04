from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QFrame, QDialogButtonBox, QApplication, QComboBox
from PyQt5.QtCore import pyqtSignal
from core import ReaderDb, isFeed, feedInfo

class FeedAddDialog(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.resize(400, 150)
        self.vLayout = QVBoxLayout(self)
        self.vLayout.setSpacing(5)
        self.vLayout.setContentsMargins(5, 5, 5, 5)
        self.labelTitle = QLabel(self)
        self.vLayout.addWidget(self.labelTitle)
        self.labelRSS = QLabel(self)
        self.vLayout.addWidget(self.labelRSS)
        self.lineEditURI = QLineEdit(self)
        self.vLayout.addWidget(self.lineEditURI)
        self.labelWarning = QLabel(self)
        self.labelWarning.hide()
        self.vLayout.addWidget(self.labelWarning)

        self.labelCategory = QLabel(self)
        self.labelCategory.setText(self.tr("Category:"))
        self.labelCategory.hide()
        self.vLayout.addWidget(self.labelCategory)
        self.comboBox = QComboBox(self)
        self.comboBox.addItem(self.tr("All Feeds"))
        self.comboBox.hide()
        self.vLayout.addWidget(self.comboBox)

        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.vLayout.addWidget(self.line)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save|QDialogButtonBox.Ok)
        self.buttonBox.button(QDialogButtonBox.Cancel).setText(self.tr("Cancel"))
        self.buttonBox.button(QDialogButtonBox.Save).setText(self.tr("Save"))
        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.feedAdd)
        self.buttonBox.button(QDialogButtonBox.Save).hide()
        self.buttonBox.button(QDialogButtonBox.Ok).setText(self.tr("Ok"))
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.feedControl)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)

        self.vLayout.addWidget(self.buttonBox)
        self.lineEditURI.textChanged.connect(self.changeText)

        self.setWindowTitle(self.tr("New Feed"))
        self.labelTitle.setText(self.tr("<span style='font-size:16pt; font-weight:bold;'>Add New Feed</span>"))
        self.labelRSS.setText(self.tr("Enter link or source of feed:"))

        url = QApplication.clipboard().text()
        if url.startswith("http://") or url.startswith("https://"):
            self.lineEditURI.setText(url)
        else: self.lineEditURI.setText("http://")
        self.lineEditURI.selectAll()

    def changeText(self):
        self.labelWarning.hide()
        self.labelCategory.hide()
        self.comboBox.hide()
        self.buttonBox.button(QDialogButtonBox.Ok).show()
        self.buttonBox.button(QDialogButtonBox.Save).hide()
        self.resize(400, 150)

    def feedControl(self):
        feed = isFeed(self.lineEditURI.text())
        if feed:
            data = feedInfo(self.lineEditURI.text())
            db = ReaderDb()
            db.execute("select * from folders where feed_url=?", (data["feedlink"],))
            if not db.cursor.fetchone():
                db.execute("select * from folders where type='folder'")
                for category in db.cursor.fetchall():
                    self.comboBox.addItem(category["title"])
                self.labelCategory.show()
                self.comboBox.show()
                self.buttonBox.button(QDialogButtonBox.Save).show()
                self.buttonBox.button(QDialogButtonBox.Ok).hide()
            else:
                self.labelWarning.setText(self.tr("<span style='color:red; font-size:15px; font-weight:bold;'>That feed is already exist!</span>"))
                self.labelWarning.show()
        else:
            self.labelWarning.setText(self.tr("<span style='color:red; font-size:15px; font-weight:bold;'>Wrong link name!</span>"))
            self.labelWarning.show()

    feedAddFinished = pyqtSignal(str)
    def feedAdd(self):
        data = feedInfo(self.lineEditURI.text())
        db = ReaderDb()
        db.execute("select id from folders where type='folder' and title=?", (self.comboBox.currentText(),))
        if db.cursor.fetchone():
            category = db.cursor.fetchone()["id"]
        else: category = 0
        print("Feedin yeni kategorisi ", category)
        db.execute("insert into folders (title, parent, type, feed_url, site_url, description) values (?, ?, 'feed', ?, ?, ?)",
                    (data["title"], category, data["feedlink"], data["sitelink"], data["description"]))
        db.commit()
        db.close()
        self.feedAddFinished.emit(self.lineEditURI.text())
        self.close()
