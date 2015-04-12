from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QFrame
from PyQt5.QtWidgets import QAbstractItemView, QTreeWidget, QTreeWidgetItem, QDialogButtonBox
from core.database import ReaderDb

class FeedFolderDialog(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.resize(400, 300)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)

        self.labelName = QLabel(self)
        self.verticalLayout.addWidget(self.labelName)
        self.lineEditFolder = QLineEdit(self)
        self.verticalLayout.addWidget(self.lineEditFolder)
        self.labelFolder = QLabel(self)
        self.verticalLayout.addWidget(self.labelFolder)
        self.treeWidget = QTreeWidget(self)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setIconSize(QSize(12, 12))
        self.treeWidget.setAnimated(True)
        #self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeWidget.header().setVisible(False)
        self.verticalLayout.addWidget(self.treeWidget)


        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.save)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)
        self.lineEditFolder.returnPressed.connect(self.buttonBox.button(QDialogButtonBox.Save).animateClick)

        self.setWindowTitle("Dizin Ekle")
        self.labelName.setText("İsim:")
        self.labelFolder.setText("Yerleşim:")

        self.treeWidget.headerItem().setText(0, "Dizin")

        categories = ReaderDb().categoryListDb()
        print(categories)
        for item in categories:
            tree = QTreeWidgetItem(self.treeWidget)
            tree.category_id = item[0]
            tree.setText(0,item[1])
            tree.subcategory = item[2]


        #self.treeWidget.topLevelItem(0).setText(0, "Tüm Beslemeler")#<-

    def save(self):
        if self.treeWidget.currentItem() == None or len(self.treeWidget.selectedItems()):
            text = self.lineEditFolder.text()
            if len(text):
                db = ReaderDb()
                db.categoryAddDb(text, 0)
                self.close()
        else:
            pass
        print(self.treeWidget.currentItem(), self.treeWidget.currentIndex(), self.treeWidget.selectedItems())