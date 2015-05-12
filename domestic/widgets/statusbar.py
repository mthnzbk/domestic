from PyQt5.QtWidgets import QStatusBar, QProgressBar, QApplication
from PyQt5.QtCore import Qt

class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super(QStatusBar, self).__init__(parent)
        self.progress = QProgressBar(self)
        self.progress.setFormat("%v/%m")
        self.progress.setTextVisible(False)
        self.progress.setMaximumWidth(200)
        self.addPermanentWidget(self.progress)
        self.counter = 0
        self.progress.hide()


    def setProgress(self):
        self.counter += 1
        self.progress.setValue(self.counter)
        if self.progress.maximum() > self.counter:
            QApplication.setOverrideCursor(Qt.BusyCursor)
            self.progress.show()
        else:
            self.progress.hide()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.counter = 0