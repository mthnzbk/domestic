from PyQt5.QtWidgets import QMenu, QAction, QApplication
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtCore import QUrl

class FileMenu(QMenu):
    def __init__(self, parent = None):
        super(QMenu, self).__init__(parent)
        self.setTitle(self.tr("File"))
        self.menuAdd = AddMenu(self)
        self.actionImport = QAction(self)
        self.actionExport = QAction(self)
        self.actionExit = QAction(self)
        self.actionExit.setIcon(QIcon(":/images/icons/exit.png"))

        self.addAction(self.menuAdd.menuAction())
        self.addSeparator()
        self.addActions((self.actionImport, self.actionExport))
        self.addSeparator()
        self.addAction(self.actionExit)

        self.actionImport.setText(self.tr("Import Feeds"))
        self.actionExport.setText(self.tr("Export Feeds"))
        self.actionExit.setText(self.tr("Exit"))
        self.actionExit.setShortcut("Ctrl+W")

class AddMenu(QMenu):
    def __init__(self, parent = None):
        super(QMenu, self).__init__(parent)
        self.setTitle(self.tr("Add"))
        self.actionFeedAdd = QAction(self)
        self.actionFeedAdd.setIcon(QIcon(":/images/icons/edit_add.png"))
        self.actionFolderAdd = QAction(self)
        self.actionFolderAdd.setIcon(QIcon(":/images/icons/folder_yellow.png"))

        self.addAction(self.actionFeedAdd)
        self.addAction(self.actionFolderAdd)

        self.actionFeedAdd.setText(self.tr("Add Feed"))
        self.actionFeedAdd.setShortcut("Ctrl+N")
        self.actionFolderAdd.setText(self.tr("Add Folder"))
        self.actionFolderAdd.setShortcut("Ctrl+Shift+N")

class FeedMenu(QMenu):
    def __init__(self, parent = None):
        super(QMenu, self).__init__(parent)
        self.setTitle(self.tr("Feeds"))
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

        self.actionAllUpdate.setText(self.tr("All Update"))
        self.actionAllUpdate.setShortcut("F5")
        self.actionDelete.setText(self.tr("Delete"))
        self.actionDelete.setShortcut("Delete")
        self.actionInfo.setText(self.tr("Info"))
        self.actionStoreAdd.setText(self.tr("Store"))

class ToolsMenu(QMenu):
    def __init__(self, parent = None):
        super(QMenu, self).__init__(parent)
        self.setTitle(self.tr("Tools"))
        self.actionSettings = QAction(self)
        self.actionSettings.setIcon(QIcon(":/images/icons/configure.png"))
        self.actionDownloaded = QAction(self)
        self.addAction(self.actionDownloaded)
        self.addSeparator()
        self.addAction(self.actionSettings)

        self.actionSettings.setEnabled(False)

        self.actionSettings.setText(self.tr("Options"))
        self.actionSettings.setShortcut("Ctrl+O")
        self.actionDownloaded.setText(self.tr("Downloads"))

class HelpMenu(QMenu):
    def __init__(self, parent = None):
        super(QMenu, self).__init__(parent)
        self.setTitle(self.tr("Help"))
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

        self.actionUpdateControl.setText(self.tr("Check for update"))
        self.actionReport.setText(self.tr("Submit Feedback"))
        self.actionQtAbout.setText(self.tr("About Qt"))
        self.actionAbout.setText(self.tr("About"))

    def openUrl(self):
        QDesktopServices.openUrl(QUrl("https://github.com/mthnzbk/domestic/issues"))