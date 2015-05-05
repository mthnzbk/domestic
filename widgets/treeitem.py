from PyQt5.QtWidgets import QTreeWidgetItem

class FolderItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        super(QTreeWidgetItem, self).__init__(parent)
        self.parent = parent
        self.id = None
        self.title = ""
        self.type = "folder"
        self.parent = 0
        self.isFolder = True


class FeedItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        super(QTreeWidgetItem, self).__init__(parent)
        self.parent = parent
        self.id = None
        self.feed_url = ""
        self.site_url = ""
        self.title = ""
        self.type = "feed"
        self.isFeed = True
        self.parent = 0
        self.description = ""
        self.favicon = None


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