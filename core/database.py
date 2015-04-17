import sqlite3 as sql
import os.path as os

from core.settings import Settings


def dbInıtıal():
    pass

class ReaderDb(object):
    def __init__(self):
        self.connect = sql.connect(os.join(os.dirname(Settings.fileName()), "Domestic.db"))
        self.cursor = self.connect.cursor()
        self.execute = self.cursor.execute
        self.commit = self.connect.commit
        self.close = self.connect.close