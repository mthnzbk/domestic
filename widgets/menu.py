from PyQt5.QtWidgets import QMenu, QAction, QApplication

class FileMenu(QMenu):
    def __init__(self, parent = None):
        super(QMenu, self).__init__(parent)
        self.setTitle("Dosya")
        self.menuAdd = AddMenu(self)
        self.actionExit = QAction(self)

        self.addAction(self.menuAdd.menuAction())
        self.addSeparator()
        self.addAction(self.actionExit)

        self.actionExit.setText("Çıkış")
        self.actionExit.setShortcut("Ctrl+W")


class AddMenu(QMenu):
    def __init__(self, parent = None):
        super(QMenu, self).__init__(parent)
        self.setTitle("Ekle")
        self.actionFeedAdd = QAction(self)
        self.actionFolderAdd = QAction(self)

        self.addAction(self.actionFeedAdd)
        self.addAction(self.actionFolderAdd)

        self.actionFeedAdd.setText("Besleme Ekle")
        self.actionFeedAdd.setShortcut("Ctrl+N")
        self.actionFolderAdd.setText("Dizin Ekle")
        self.actionFolderAdd.setShortcut("Ctrl+Shift+N")

class FeedMenu(QMenu):
    def __init__(self, parent = None):
        super(QMenu, self).__init__(parent)
        self.setTitle("Beslemeler")
        self.actionRefresh = QAction(self)
        self.actionFeedRefresh = QAction(self)
        self.actionDelete = QAction(self)
        self.actionPreference = QAction(self)
        self.actionReadMark = QAction(self)
        self.actionStoreAdd = QAction(self)

        self.addAction(self.actionFeedRefresh)
        self.addAction(self.actionRefresh)
        self.addSeparator()
        self.addAction(self.actionReadMark)
        self.addAction(self.actionStoreAdd)
        self.addAction(self.actionDelete)
        self.addSeparator()
        self.addAction(self.actionPreference)

        self.actionRefresh.setText("Tümünü güncelle")
        self.actionRefresh.setShortcut("Ctrl+F5")
        self.actionFeedRefresh.setText("Besleme güncelle")
        self.actionFeedRefresh.setShortcut("F5")
        self.actionDelete.setText("Sil")
        self.actionPreference.setText("Özellikler")
        self.actionReadMark.setText("Okundu/Okunmadı olarak işaretle")
        self.actionStoreAdd.setText("Sakla")

class ToolsMenu(QMenu):
    def __init__(self, parent = None):
        super(QMenu, self).__init__(parent)
        self.setTitle("Araçlar")
        self.actionSettings = QAction(self)
        self.actionDownloaded = QAction(self)
        self.addAction(self.actionDownloaded)
        self.addSeparator()
        self.addAction(self.actionSettings)

        self.actionSettings.setText("Seçenekler")
        self.actionSettings.setShortcut("Ctrl+O")
        self.actionDownloaded.setText("İndirilenler")

class HelpMenu(QMenu):
    def __init__(self, parent = None):
        super(QMenu, self).__init__(parent)
        self.setTitle("Yardım")
        self.actionUpdateControl = QAction(self)
        self.actionReport = QAction(self)
        self.actionAbout = QAction(self)
        self.actionQtAbout = QAction(self)
        self.actionQtAbout.triggered.connect(QApplication.aboutQt)

        self.addAction(self.actionUpdateControl)
        self.addSeparator()
        self.addAction(self.actionReport)
        self.addAction(self.actionQtAbout)
        self.addAction(self.actionAbout)

        self.actionUpdateControl.setText("Güncellemeyi kontrol et")
        self.actionReport.setText("Sorun bildir")
        self.actionQtAbout.setText("Qt Hakkında")
        self.actionAbout.setText("Hakkında")