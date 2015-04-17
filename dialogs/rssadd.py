from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QFrame, QDialogButtonBox, QApplication
from core import isRSS, feedInfo, ReaderDb
from PyQt5.QtCore import pyqtSignal

class RSSAddDialog(QDialog):
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
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.vLayout.addWidget(self.line)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.button(QDialogButtonBox.Cancel).setText(self.tr("Vazgeç"))
        self.buttonBox.button(QDialogButtonBox.Save).setText(self.tr("Kaydet"))
        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.rssAdd)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)

        self.vLayout.addWidget(self.buttonBox)
        self.lineEditURI.returnPressed.connect(self.buttonBox.button(QDialogButtonBox.Save).toggle)
        self.lineEditURI.textChanged.connect(self.labelWarning.hide)

        self.setWindowTitle(self.tr("Yeni Besleme"))
        self.labelTitle.setText(self.tr("<span style='font-size:16pt; font-weight:bold;'>Yeni Besleme Ekle</span>"))
        self.labelRSS.setText(self.tr("Besleme bağlantısı veya kaynağını girin:"))

        url = QApplication.clipboard().text()
        if url.startswith("http://"):
            self.lineEditURI.setText(url)
        else: self.lineEditURI.setText("http://")
        self.lineEditURI.selectAll()

    rssAddFinished = pyqtSignal()
    def rssAdd(self):
        rss = isRSS(self.lineEditURI.text())
        if rss:
            data = feedInfo(self.lineEditURI.text())
            db = ReaderDb()
            control = db.execute("select * from feeds where url='{}'".format(data[1]))
            if not control.fetchone():
                db.execute("insert into feeds (site_url, url, title, description) values ('{}','{}','{}', '{}')"
                           .format(data[0], data[1],data[2], data[3]))
                db.commit()
                db.close()
                self.rssAddFinished.emit()
                self.close()
            else:
                self.labelWarning.setText(self.tr("<span style='color:red; font-size:15px; font-weight:bold;'>Bu besleme zaten mevcut!</span>"))
                self.labelWarning.show()
                print("Aynı rss yi giremezsin!")
        else:
            self.labelWarning.setText(self.tr("<span style='color:red; font-size:15px; font-weight:bold;'>Yanlış bağlantı adı girdiniz!</span>"))
            self.labelWarning.show()


