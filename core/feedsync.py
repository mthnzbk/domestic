from PyQt5.QtCore import QThread
from feedparser import parse
from core.database import ReaderDb
import time
import feedparser

class FeedSync(QThread):
    def __init__(self, parent=None):
        super(QThread, self).__init__(parent)

    def feedAdd(self, feed):
        self.feed = feed

    def convert(self, data):
        if type(data) == list:
            if "term" in data[0]:
                return data[0].term
            elif "value" in data[0]:
                return data[0].value

        elif type(data) == feedparser.FeedParserDict:
            return data.value

        else:
            return " "

    def run(self):
        for feed in self.feed:
            feedData = parse(feed[0])
            entries = feedData.entries
            db = ReaderDb()
            for entry in entries:
                print(entry.link)
                control = db.execute("select * from store where entry_url=?", (entry.link,))
                data = control.fetchone()
                if data:
                    print("{} mevcut".format(feedData.feed.title))
                elif not data:
                    print(entry.get("tags", " "), "LAHAB")
                    entry_publish = time.strftime("%d.%m.%Y %H:%M", entry.published_parsed)
                    feed_url, feed_title, entry_url, entry_title = feedData.href, feedData.feed.title, entry.link, entry.title
                    entry_author, entry_category, entry_datetime, entry_content = entry.get('author',' '), self.convert(entry.get("tags", " ")), entry_publish, self.convert(entry.get("content", entry.summary_detail))
                    db.execute("insert into store (feed_url, feed_title, entry_url, entry_title, entry_author, entry_category,"
                                        "entry_datetime, entry_content) values (?, ?, ?, ?, ?, ?, ?, ?)",
                        (feed_url, feed_title, entry_url, entry_title, entry_author, entry_category, entry_datetime, entry_content))
                    db.commit()

                else: print("entry girilmedi.", entry.link)
            db.close()