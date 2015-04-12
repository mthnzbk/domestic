from PyQt5.QtWidgets import QToolBar


class ToolBar(QToolBar):
    def __init__(self, parent=None):
        super(QToolBar, self).__init__(parent)
        self.setMovable(False)