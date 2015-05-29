import sqlite3 as sql
import os.path as os
from domestic.core.settings import Settings

def isDbExist():
    return os.isfile(os.join(os.dirname(Settings.fileName()), "Domestic.db"))

def initialDb():
    if isDbExist():
        pass
    else:
        createDb = sql.connect(os.join(os.dirname(Settings.fileName()), "Domestic.db"))
        sqlcode = """create table folders (
        id integer primary key autoincrement not null,
        title text not null,
        parent integer default 0,
        type text not null,
        feed_url text,
        site_url text,
        description text,
        favicon blob
        );
        create table store (
        id integer primary key autoincrement not null,
        feed_url text not null,
        feed_title text not null,
        entry_url text not null,
        entry_title text not null,
        entry_author text not null,
        entry_category text not null,
        entry_datetime text not null,
        entry_content text not null,
        isstore integer default 0,
        istrash integer default 0,
        iscache integer default 1,
        enclosure_length text,
        enclosure_type text,
        enclosure_url text
        );"""
        createDb.executescript(sqlcode)
        createDb.commit()
        createDb.close()

class ReaderDb(object):
    def __init__(self):
        self.connect = sql.connect(os.join(os.dirname(Settings.fileName()), "Domestic.db"))
        self.connect.row_factory = sql.Row
        self.cursor = self.connect.cursor()
        self.execute = self.cursor.execute
        self.executemany = self.cursor.executemany
        self.commit = self.connect.commit
        self.close = self.connect.close