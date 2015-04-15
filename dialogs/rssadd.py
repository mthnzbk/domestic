from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QFrame, QDialogButtonBox, QApplication
from core import isRSS, rssGetInfo, ReaderDb
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
        self.labelWarning.setText("<span style='color:red; font-size:15px; font-weight:bold;'>Yanlış bağlantı adı girdiniz!</span>")
        self.labelWarning.hide()
        self.vLayout.addWidget(self.labelWarning)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.vLayout.addWidget(self.line)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Vazgeç")
        self.buttonBox.button(QDialogButtonBox.Save).setText("Kaydet")
        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.rssAdd)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)

        self.vLayout.addWidget(self.buttonBox)
        self.lineEditURI.returnPressed.connect(self.buttonBox.button(QDialogButtonBox.Save).toggle)
        self.lineEditURI.textChanged.connect(self.labelWarning.hide)

        self.setWindowTitle("Yeni Besleme")
        self.labelTitle.setText("<span style='font-size:16pt; font-weight:bold;'>Yeni Besleme Ekle</span>")
        self.labelRSS.setText("Besleme bağlantısı veya kaynağını girin:")

        url = QApplication.clipboard().text()
        if url.startswith("http://"):
            self.lineEditURI.setText(url)
        else: self.lineEditURI.setText("http://")
        self.lineEditURI.selectAll()

    rssAddFinished = pyqtSignal()
    def rssAdd(self):
        rss = isRSS(self.lineEditURI.text())
        if rss:
            data = rssGetInfo(self.lineEditURI.text())
            db = ReaderDb()
            control = db.execute("select * from feeds where url='{}'".format(data[0]))
            if not control.fetchone():
                db.execute("insert into feeds (url, title) values ('{}','{}')".format(data[0], data[1]))
                db.commit()
                db.close()
                self.rssAddFinished.emit()
                self.close()
            else:
                print("Aynı rss yi giremezsin!") #Daha sonra QMessageBox Eklenecek.
        else:
            self.labelWarning.show()


