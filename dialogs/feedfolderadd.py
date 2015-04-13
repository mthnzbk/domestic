from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QFrame
from PyQt5.QtWidgets import QAbstractItemView, QTreeWidget, QTreeWidgetItem, QDialogButtonBox, QMessageBox
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
        self.labelWarning = QLabel(self)

        self.labelWarning.setText("<span style='color:red; font-size:15px; font-weight:bold; align:'center';'>Dizin adı girmediniz!</span>")
        self.labelWarning.hide()
        self.verticalLayout.addWidget(self.labelWarning)
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
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Vazgeç")
        self.buttonBox.button(QDialogButtonBox.Save).setText("Kaydet")
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.save)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)
        self.lineEditFolder.returnPressed.connect(self.buttonBox.button(QDialogButtonBox.Save).click)
        self.lineEditFolder.textChanged.connect(self.labelWarning.hide)

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

    def save(self):
        text = self.lineEditFolder.text()
        db = ReaderDb()
        if len(text):
            if self.treeWidget.currentItem() == None or len(self.treeWidget.selectedItems()):
                db.categoryAddDb(text, 0)
                self.close()
            else:
                selectItem = self.treeWidget.currentItem()
                db.categoryAddDb(text, selectItem.subcategory)
                self.close()
        else:
            self.labelWarning.show()

