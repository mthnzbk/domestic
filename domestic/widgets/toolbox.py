from PyQt5.QtWidgets import QToolBox

class ToolBox(QToolBox):
    def __init__(self, parent=None):
        super(QToolBox, self).__init__(parent)
        self.currentChanged.connect(self.widgetFocus)

    def widgetFocus(self, widget):
        if not widget:
            self.widget(widget).treeWidget.setFocus()