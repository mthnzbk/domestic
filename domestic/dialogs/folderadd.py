from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QFrame
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QDialogButtonBox
from domestic.core.database import ReaderDb


class FolderDialog(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.parent = parent
        self.resize(400, 300)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)

        self.labelName = QLabel(self)
        self.verticalLayout.addWidget(self.labelName)
        self.lineEditFolder = QLineEdit(self)
        self.verticalLayout.addWidget(self.lineEditFolder)
        self.labelWarning = QLabel(self)
        self.labelWarning.hide()
        self.verticalLayout.addWidget(self.labelWarning)
        self.labelFolder = QLabel(self)
        self.verticalLayout.addWidget(self.labelFolder)
        self.treeWidget = QTreeWidget(self)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setIconSize(QSize(12, 12))
        self.treeWidget.setAnimated(True)
        self.treeWidget.header().setVisible(False)
        self.verticalLayout.addWidget(self.treeWidget)


        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.button(QDialogButtonBox.Cancel).setText(self.tr("Cancel"))
        self.buttonBox.button(QDialogButtonBox.Save).setText(self.tr("Save"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.folderAdd)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)
        self.lineEditFolder.returnPressed.connect(self.buttonBox.button(QDialogButtonBox.Save).toggle)
        self.lineEditFolder.textChanged.connect(self.labelWarning.hide)

        self.setWindowTitle(self.tr("Add Folder"))
        self.labelName.setText(self.tr("Name:"))
        self.labelFolder.setText(self.tr("Insert:"))
        self.treeWidget.headerItem().setText(0, self.tr("Folder"))
        self.treeWidget.setIconSize(QSize(18, 18))

        self.categorySorting(treeitem=self.treeWidget)

    def categorySorting(self, id=0, treeitem=None):
        db = ReaderDb()
        db.execute("select * from folders where type='folder' and parent=?",(id,))
        folders = db.cursor.fetchall()
        for folder in folders:
            item = QTreeWidgetItem(treeitem)
            item.setIcon(0, QIcon(":/images/icons/folder_grey.png"))
            item.id = folder["id"]
            item.category_name = folder[1]
            item.setText(0, item.category_name)
            item.subcategory = folder["parent"]
            self.categorySorting(folder["id"], item)

    def folderAdd(self):
        text = self.lineEditFolder.text()
        db = ReaderDb()
        if len(text):
            control = db.execute("select * from folders where title=?", (text,))
            if not control.fetchone():
                if self.treeWidget.currentItem() == None or not len(self.treeWidget.selectedItems()):
                    db.execute("insert into folders (title, type) values (?, 'folder')", (text,))
                    db.commit()
                    db.close()
                else:
                    db.execute("insert into folders (title, parent, type) values (?, ?, 'folder')", (text, self.treeWidget.currentItem().id))
                    db.commit()
                    db.close()
                self.parent.syncSignal.emit()
                self.parent.categorySync()
                self.close()
            else:
                self.labelWarning.setText(self.tr("<span style='color:red; font-size:15px; font-weight:bold;'>Same category name cannot add!</span>"))
                self.labelWarning.show()
        else:
            self.labelWarning.setText(self.tr("<span style='color:red; font-size:15px; font-weight:bold; align:'center';'>You didn't write folder's name!</span>"))
            self.labelWarning.show()

