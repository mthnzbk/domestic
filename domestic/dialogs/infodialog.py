from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QFormLayout, QDialogButtonBox, QComboBox
from domestic.core import ReaderDb


class InfoDialog(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.parent = parent
        self.resize(360, 180)
        self.formLayout = QFormLayout(self)
        self.labelTitle = QLabel(self)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelTitle)
        self.lineEditTitle = QLineEdit(self)
        self.lineEditTitle.setClearButtonEnabled(True)
        self.lineEditTitle.setReadOnly(True)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEditTitle)
        self.labelFeed = QLabel(self)
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelFeed)
        self.lineEditFeed = QLineEdit(self)
        self.lineEditFeed.setReadOnly(True)
        self.lineEditFeed.setClearButtonEnabled(True)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEditFeed)
        self.labelMain = QLabel(self)
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelMain)
        self.labelMainURL = QLabel(self)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.labelMainURL)
        self.labelCategory = QLabel(self)
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.labelCategory)
        self.comboBox = QComboBox(self)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.comboBox)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.buttonBox)

        self.buttonBox.accepted.connect(self.saveInfo)
        self.labelMainURL.linkActivated.connect(self.openURL)

        self.labelTitle.setText(self.tr("Title:"))
        self.labelFeed.setText(self.tr("Feed URL:"))
        self.labelMain.setText(self.tr("Main Page:"))
        self.labelCategory.setText(self.tr("Category:"))
        self.comboBox.addItem(self.tr("All Feeds"))

    def saveInfo(self):
        db = ReaderDb()
        db.execute("select * from folders where type='folder' and title=?", (self.comboBox.currentText(),))
        data = db.cursor.fetchone()
        if data:
            category = data["id"]
        else: category = 0
        db.execute("update folders set parent=? where id=?", (category, self.item.id))
        db.commit()
        db.close()
        self.parent.syncSignal.emit()
        self.parent.categorySync()
        self.accept()

    def openURL(self, text):
        QDesktopServices.openUrl(QUrl(text))

    def addItem(self, item):
        self.item = item
        self.setWindowTitle(self.tr("{} - Info").format(self.item.title))
        self.lineEditFeed.setText(self.item.feed_url)
        self.lineEditTitle.setText(self.item.title)
        self.labelMainURL.setText("<a href='{0}'>{0}</a>".format(self.item.site_url))
        db = ReaderDb()
        db.execute("select * from folders where type='folder'")
        categories = db.cursor.fetchall()
        for category in categories:
            self.comboBox.addItem(category["title"])
            if item.parent == category["id"]:
                self.comboBox.setCurrentText(category["title"])


    def getItem(self):
        return self.item