from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QFrame
from PyQt5.QtWidgets import QAbstractItemView, QTreeWidget, QTreeWidgetItem, QDialogButtonBox, QMessageBox
from core.database import ReaderDb

class RSSFolderDialog(QDialog):
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

        self.labelWarning.setText(self.tr("<span style='color:red; font-size:15px; font-weight:bold; align:'center';'>Dizin adı girmediniz!</span>"))
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
        self.buttonBox.button(QDialogButtonBox.Cancel).setText(self.tr("Vazgeç"))
        self.buttonBox.button(QDialogButtonBox.Save).setText(self.tr("Kaydet"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.folderAdd)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)
        self.lineEditFolder.returnPressed.connect(self.buttonBox.button(QDialogButtonBox.Save).toggle)
        self.lineEditFolder.textChanged.connect(self.labelWarning.hide)

        self.setWindowTitle(self.tr("Dizin Ekle"))
        self.labelName.setText(self.tr("İsim:"))
        self.labelFolder.setText(self.tr("Yerleşim:"))
        self.treeWidget.headerItem().setText(0, self.tr("Dizin"))
        self.treeWidget.setIconSize(QSize(24, 24))

        self.categorySorting()
        print(self.treeWidget.selectedItems())

    def categorySorting(self):
        db = ReaderDb()
        control = db.execute("select * from categories where subcategory=0")
        maincategories = control.fetchall()
        for maincategory in maincategories:
            maintree = QTreeWidgetItem(self.treeWidget)
            maintree.setIcon(0, QIcon(":/images/icons/folder_grey.png"))
            maintree.id = maincategory[0]
            maintree.category_name = maincategory[1]
            maintree.setText(0,maintree.category_name)
            maintree.subcategory = maincategory[2]
            control = db.execute("select * from categories where subcategory=?", (maintree.id,))
            subcategories = control.fetchall()
            print(maintree.id, maintree.subcategory, subcategories)
            if subcategories:
                for subcategory in subcategories:
                    subtree = QTreeWidgetItem(maintree)
                    maintree.addChild(subtree)
                    subtree.setIcon(0, QIcon(":/images/icons/folder_grey.png"))
                    subtree.id = subcategory[0]
                    subtree.category_name = subcategory[1]
                    subtree.setText(0,subtree.category_name)
                    subtree.subcategory = subcategory[2]
            else:
                continue

    folderAddFinished = pyqtSignal()
    def folderAdd(self):
        text = self.lineEditFolder.text()
        db = ReaderDb()
        if len(text):
            control = db.execute("select * from categories where category_name=?", (text,))
            if not control.fetchone():
                print(self.treeWidget.currentItem() == None, not len(self.treeWidget.selectedItems()))
                if self.treeWidget.currentItem() == None or not len(self.treeWidget.selectedItems()):
                    db.execute("insert into categories (category_name) values (?)", (text,))
                    db.commit()
                    db.close()
                else:
                    print(self.treeWidget.currentItem().id)
                    db.execute("insert into categories (category_name, subcategory) values (?, ?)", (text,self.treeWidget.currentItem().id))
                    db.commit()
                    db.close()
                self.folderAddFinished.emit()
                self.close()
            else:
                print("Aynı kategori ismi eklenemiyor :(") # daha sonra gereken uyarı eklenecek
        else:
            self.labelWarning.show()

