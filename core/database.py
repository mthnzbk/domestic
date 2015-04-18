import sqlite3 as sql
import os.path as os
from core.settings import Settings

def isDbExist():
    return os.isfile(os.join(os.dirname(Settings.fileName()), "Domestic.db"))

def inıtıalDb():
    if isDbExist():
        pass
    else:
        createDb = sql.connect(os.join(os.dirname(Settings.fileName()), "Domestic.db"))
        sqlcode = """create table categories (
        id integer primary key autoincrement not null,
        category_name text not null,
        subcategory integer default 0
        )"""
        sqlcode1 = """create table feeds (
        id integer primary key autoincrement not null,
        site_url text not null,
        url text not null,
        title text not null,
        category integer default 0,
        description text default ''
        )"""
        sqlcode2 = """create table store (
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
        iscache integer default 1
        )"""
        createDb.execute(sqlcode)
        createDb.execute(sqlcode1)
        createDb.execute(sqlcode2)
        createDb.commit()
        createDb.close()

class ReaderDb(object):
    def __init__(self):
        self.connect = sql.connect(os.join(os.dirname(Settings.fileName()), "Domestic.db"))
        self.cursor = self.connect.cursor()
        self.execute = self.cursor.execute
        self.commit = self.connect.commit
        self.close = self.connect.close