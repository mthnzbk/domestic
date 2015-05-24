from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtGui import QIcon, QPixmap, QColor, QBrush
from domestic.core import ReaderDb

class FolderItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        super(QTreeWidgetItem, self).__init__(parent)
        self._parent = parent
        self.setIcon(0, QIcon(":/images/icons/folder_grey.png"))

    def folderClick(self):
        feedList = self.folderInit()
        if len(feedList) > 0:
            self.setText(0, "({}) {}".format(len(feedList), self.title))
        else: self.setText(0, self.title)
        self.newsCount = 0
        self.feedList.clear()
        self.entryList.clear()

    entryList = []
    def folderInit(self): #FIXME
        db = ReaderDb()
        self.categorySorting(self.id)
        for feed in self.feedList:
            db.execute("select * from store where iscache=1 and feed_url=?", feed)
            for entry in db.cursor.fetchall():
                self.entryList.append(entry)
        self.setForeground(0,QBrush(QColor(0,0,0,255)))
        if self.newsCount > 0:
            self.setText(0, "({}) {}".format(self.newsCount, self.title))
            self.setForeground(0,QBrush(QColor(0,0,255)))
        return self.entryList

    newsCount = 0
    feedList = []
    def categorySorting(self, id=0):
        db = ReaderDb()
        db.execute("select * from folders where parent=?",(id,))
        folders = db.cursor.fetchall()
        for feed in folders:
            if feed["type"] == "feed":
                db.execute("select * from store where iscache=1 and feed_url=?", (feed["feed_url"],))
                data = db.cursor.fetchall()
                self.feedList.append((feed["feed_url"],))
                self.newsCount += len(data)
            self.categorySorting(feed["id"])

    def addOptions(self, options):
        self.id = options["id"]
        self.title = options["title"]
        self.type = options["type"]
        self.setText(0, self.title)
        self.parent = options["parent"]
        self.folderInit()

class FeedItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        super(QTreeWidgetItem, self).__init__(parent)
        self._parent = parent

    def feedClick(self):
        feedList = self.feedInit()
        if len(feedList) > 0:
            self.setText(0, "({}) {}".format(len(feedList), self.title))
        else: self.setText(0, self.title)

    def feedInit(self):
        db = ReaderDb()
        data = db.execute("select * from store where iscache=1 and feed_url=?", (self.feed_url,))
        feedList = data.fetchall()
        db.close()
        self.setForeground(0,QBrush(QColor(0,0,0,255)))
        if len(feedList) > 0:
            self.setText(0, "({}) {}".format(len(feedList), self.title))
            self.setForeground(0,QBrush(QColor(0,0,255)))
        return feedList

    def addOptions(self, options):
        self.id = options["id"]
        self.title = options["title"]
        self.setText(0, self.title)
        self.parent = options["parent"]
        self.feed_url = options["feed_url"]
        self.site_url = options["site_url"]
        self.type = options["type"]
        self.description = options["description"]
        self.favicon = options["favicon"]
        if not self.favicon is None:
            icon = QIcon()
            pix = QPixmap()
            pix.loadFromData(self.favicon)
            icon.addPixmap(pix)
            self.setIcon(0, icon)
        else:
            self.setIcon(0, QIcon(":/images/icons/html.png"))
        self.feedInit()

class EntryItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        super(QTreeWidgetItem, self).__init__(parent)

    def id(self, id):
        self.id = id

    def feedUrl(self, url):
        self.feedurl = url

    def getFeedUrl(self):
        return self.feedurl

    def feedTitle(self, title):
        self.feedtitle = title
        self.setText(0, title)
        self.setToolTip(0, title)

    def getFeedTitle(self):
        return  self.feedtitle

    def entryUrl(self, url):
        self.entryurl= url

    def getEntryUrl(self):
        return self.entryurl

    def entryTitle(self, title):
        self.entrytitle = title
        self.setText(1, title)
        self.setToolTip(1, title)

    def getEntryTitle(self):
        return self.entrytitle

    def entryAuthor(self, author):
        self.entryauthor = author
        self.setText(2, author)
        self.setToolTip(2, author)

    def getEntryAuthor(self):
        return self.entryauthor

    def entryCategory(self, category):
        self.entrycategory = category
        self.setText(3, category)
        self.setToolTip(3, category)

    def getEntryCategory(self):
        return  self.entrycategory

    def entryDateTime(self, datetime):
        self.entrydatetime = datetime
        self.setText(4, datetime)
        self.setToolTip(4, datetime)

    def getEntryDateTime(self):
        return self.entrydatetime

    def entryContent(self, content):
        self.entrycontent = content

    def getEntryContent(self):
        return self.entrycontent