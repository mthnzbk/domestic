import sqlite3 as sql
from widgets.settings import Settings
import os.path as os

def dbInıtıal():
    pass

class ReaderDb(object):
    def __init__(self):
        self.connect = sql.connect(os.join(os.dirname(Settings.fileName()), "reader.db"))
        self.cursor = self.connect.cursor()
        self.execute = self.cursor.execute

    def feedAddDb(self, url, title):
        self.execute("insert into feeds (url, title) values ('{}', '{}')".format(url, title))
        self.connect.commit()
        self.connect.close()

    def rssList(self): # Tümünü güncelle
        data = self.execute("select url from feeds")
        data = data.fetchall()
        return data

    def feedsList(self):
        data = self.execute("select site_title, feed_title, feed_author, feed_datetime, feed_category, feed_url, feed_content from store where iscache=1")
        data = data.fetchall()
        return data

    def updateFeed(self, feedList):
        for feed in feedList:
            print(feed)
            self.execute("insert into store (feed_url, site_title, feed_title, feed_author, feed_datetime, feed_category, feed_content) \
            values ('{}','{}','{}','{}','{}','{}','{}');".format(feed[0],feed[1],feed[2],feed[3],feed[4],feed[5],feed[6]))
            self.connect.commit()
        self.connect.close()

    def allFeed(self):
        data = self.execute("select url, title from feeds")
        data = data.fetchall()
        self.connect.close()
        return data

    def categoryAddDb(self, category, scategory):
        self.execute("insert into categories (category_name, subcategory) values ('{}', {})".format(category, scategory))
        self.connect.commit()
        self.connect.close()

    def categoryListDb(self): # Dizin ekleme de listeleme için kullanılıyor
        data = self.execute("select * from categories")
        data = data.fetchall()
        self.connect.close()
        return data

    def deletedFeeds(self):
        data = self.execute("select * from store where istrash=1")
        data = data.fetchall()
        self.connect.close()
        return data

    def storeFeeds(self):
        data = self.execute("select * from store where isstore=1")
        data = data.fetchall()
        self.connect.close()
        return data

    def readAllFeedDb(self):
        data = self.execute()
