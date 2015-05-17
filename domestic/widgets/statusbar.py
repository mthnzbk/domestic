from PyQt5.QtWidgets import QStatusBar, QProgressBar, QApplication

class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super(QStatusBar, self).__init__(parent)
        self.parent = parent
        self.progress = QProgressBar(self)
        self.progress.setFormat("%v/%m")
        self.progress.setTextVisible(False)
        self.progress.setMaximumWidth(200)
        self.addPermanentWidget(self.progress)
        self.count = 0
        self.progress.hide()

    def setProgress(self):
        self.count += 1
        self.progress.setValue(self.count)
        if self.progress.maximum() > self.count:
            self.progress.show()
        else:
            QApplication.restoreOverrideCursor()
            self.progress.hide()
            self.count = 0