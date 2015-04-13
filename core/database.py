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

    def feedListDb(self):
        data = self.execute("select (url) from feeds")
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

    def readAllFeedDb(self):
        data = self.execute()
