import time

from PyQt5.QtCore import QThread, pyqtSignal
from feedparser import parse

from domestic.core.database import ReaderDb


class GetEntry(object):
    def __init__(self, entry, feed):
        self.entry = entry
        self.feed = feed

    def getPublish(self):
        return time.strftime("%d.%m.%Y %H:%M", self.entry.published_parsed)

    def getFeedUrl(self):
        return self.feed.href

    def getFeedTitle(self):
        return self.feed.feed.title

    def getLink(self):
        return self.entry.link

    def getTitle(self):
        return self.entry.title

    def getAuthor(self):
        return self.entry.get("author", "")

    def getCategory(self):
        if not self.entry.get("tags") is None:
            return self.entry.tags[0].term
        else:
            return ""

    def getContent(self):
        if not self.entry.get("content") is None:
            return self.entry.content[0].value

        elif not self.entry.get("summary") is None:
            return self.entry.summary

        elif not self.entry.get("summary_detail") is None:
            return self.entry.summary_detail.value

        else:
            return ""

class FeedSync(QThread):
    def __init__(self, parent=None):
        super(QThread, self).__init__(parent)

    def feedAdd(self, feed):
        self.feed = feed

    isData = pyqtSignal(bool)
    def run(self):
        feedData = parse(self.feed["feed_url"])
        entries = feedData.entries
        db = ReaderDb()
        datain = False
        entryDataList = []
        for entry in entries:
            control = db.execute("select * from store where entry_url=?", (entry.link,))
            data = control.fetchone()
            if data:
                print("{} mevcut".format(feedData.feed.title))
            elif not data:
                print(entry.link, "eklendi.")
                datain = True
                getEntry = GetEntry(entry, feedData)
                entryData = (getEntry.getFeedUrl(), getEntry.getFeedTitle(), getEntry.getLink(), getEntry.getTitle(),
                             getEntry.getAuthor(), getEntry.getCategory(), getEntry.getPublish(), getEntry.getContent())
                entryDataList.append(entryData)
            else: print("entry girilmedi.", entry.link)
        db.executemany("""insert into store (feed_url, feed_title, entry_url, entry_title, entry_author, entry_category,
                           entry_datetime, entry_content) values (?, ?, ?, ?, ?, ?, ?, ?)""", entryDataList)
        db.commit()
        self.isData.emit(datain)
        db.close()