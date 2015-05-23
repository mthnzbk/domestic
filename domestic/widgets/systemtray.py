from PyQt5.QtWidgets import QSystemTrayIcon, QApplication
from domestic.widgets.menu import *
from domestic.core import ReaderDb

class SystemTray(QSystemTrayIcon):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setVisible(True)
        self.setIcon(QIcon(":/images/rss-icon-128.png"))

        self.updateToolTip()

        self.activated.connect(self.parentShow)
        self.messageClicked.connect(self.parentShow)

    def updateToolTip(self):
        db = ReaderDb()
        db.execute("select * from store where iscache=1")
        unread = db.cursor.fetchall()
        db.execute("select * from store where isstore=1")
        store = db.cursor.fetchall()
        db.execute("select * from store where istrash=1")
        trash = db.cursor.fetchall()
        self.setToolTip(self.tr('''<span style='font-size:14pt'>{} - {}</span>
        <br><span style='font-size:10pt'>Unread: {}</span>
        <br><span style='font-size:10pt'>Stored: {}</span>
        <br><span style='font-size:10pt'>Deleted: {}</span>''').format(QApplication.applicationName(),
        QApplication.applicationVersion(), len(unread), len(store), len(trash)))

    def parentShow(self):
        self.parent.show()
