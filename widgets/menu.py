from PyQt5.QtWidgets import QMenu, QAction, QApplication
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtCore import QUrl

class FileMenu(QMenu):
    def __init__(self, parent = None):
        super(QMenu, self).__init__(parent)
        self.setTitle(self.tr("Dosya"))
        self.menuAdd = AddMenu(self)
        self.actionImport = QAction(self)
        self.actionImport.setDisabled(True)
        self.actionExport = QAction(self)
        self.actionExport.setDisabled(True)
        self.actionExit = QAction(self)
        self.actionExit.setIcon(QIcon(":/images/icons/exit.png"))

        self.addAction(self.menuAdd.menuAction())
        self.addSeparator()
        self.addActions((self.actionImport, self.actionExport))
        self.addSeparator()
        self.addAction(self.actionExit)

        self.actionImport.setText(self.tr("Beslemeleri İçeri Aktar"))
        self.actionExport.setText(self.tr("Beslemeleri Dışarı Aktar"))
        self.actionExit.setText(self.tr("Çıkış"))
        self.actionExit.setShortcut("Ctrl+W")

class AddMenu(QMenu):
    def __init__(self, parent = None):
        super(QMenu, self).__init__(parent)
        self.setTitle(self.tr("Ekle"))
        self.actionFeedAdd = QAction(self)
        self.actionFeedAdd.setIcon(QIcon(":/images/icons/edit_add.png"))
        self.actionFolderAdd = QAction(self)
        self.actionFolderAdd.setIcon(QIcon(":/images/icons/folder_yellow.png"))

        self.addAction(self.actionFeedAdd)
        self.addAction(self.actionFolderAdd)

        self.actionFeedAdd.setText(self.tr("Besleme Ekle"))
        self.actionFeedAdd.setShortcut("Ctrl+N")
        self.actionFolderAdd.setText(self.tr("Dizin Ekle"))
        self.actionFolderAdd.setShortcut("Ctrl+Shift+N")

class FeedMenu(QMenu):
    def __init__(self, parent = None):
        super(QMenu, self).__init__(parent)
        self.setTitle(self.tr("Beslemeler"))
        self.actionAllUpdate = QAction(self)
        self.actionAllUpdate.setIcon(QIcon(":/images/icons/reload.png"))
        self.actionDelete = QAction(self)
        self.actionDelete.setIcon(QIcon(":/images/icons/button_cancel.png"))
        self.actionInfo = QAction(self)
        self.actionInfo.setIcon(QIcon(":/images/icons/info.png"))
        self.actionStoreAdd = QAction(self)
        self.actionStoreAdd.setIcon(QIcon(":/images/icons/folder_tar.png"))

        self.addAction(self.actionAllUpdate)
        self.addSeparator()
        self.addAction(self.actionStoreAdd)
        self.addAction(self.actionDelete)
        self.addSeparator()
        self.addAction(self.actionInfo)

        self.actionAllUpdate.setText(self.tr("Tümünü güncelle"))
        self.actionAllUpdate.setShortcut("F5")
        self.actionDelete.setText(self.tr("Sil"))
        self.actionDelete.setShortcut("Delete")
        self.actionInfo.setText(self.tr("Özellikler"))
        self.actionStoreAdd.setText(self.tr("Sakla"))

class ToolsMenu(QMenu):
    def __init__(self, parent = None):
        super(QMenu, self).__init__(parent)
        self.setTitle(self.tr("Araçlar"))
        self.actionSettings = QAction(self)
        self.actionSettings.setIcon(QIcon(":/images/icons/configure.png"))
        self.actionDownloaded = QAction(self)
        self.addAction(self.actionDownloaded)
        self.addSeparator()
        self.addAction(self.actionSettings)

        self.actionDownloaded.setEnabled(False)
        self.actionSettings.setEnabled(False)

        self.actionSettings.setText(self.tr("Seçenekler"))
        self.actionSettings.setShortcut("Ctrl+O")
        self.actionDownloaded.setText(self.tr("İndirilenler"))

class HelpMenu(QMenu):
    def __init__(self, parent = None):
        super(QMenu, self).__init__(parent)
        self.setTitle(self.tr("Yardım"))
        self.actionUpdateControl = QAction(self)
        self.actionUpdateControl.setDisabled(True)
        self.actionReport = QAction(self)
        self.actionReport.setIcon(QIcon(":/images/icons/web.png"))
        self.actionReport.triggered.connect(self.openUrl)
        self.actionAbout = QAction(self)
        self.actionQtAbout = QAction(self)
        self.actionQtAbout.triggered.connect(QApplication.aboutQt)

        self.addAction(self.actionUpdateControl)
        self.addSeparator()
        self.addAction(self.actionReport)
        self.addAction(self.actionQtAbout)
        self.addAction(self.actionAbout)

        self.actionUpdateControl.setText(self.tr("Güncellemeyi kontrol et"))
        self.actionReport.setText(self.tr("Sorun bildir"))
        self.actionQtAbout.setText(self.tr("Qt Hakkında"))
        self.actionAbout.setText(self.tr("Hakkında"))

    def openUrl(self):
        QDesktopServices.openUrl(QUrl("https://github.com/mthnzbk/domestic-reader/issues"))