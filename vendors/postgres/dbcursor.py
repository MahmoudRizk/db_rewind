from dbrewinder import dbcursor_interface
from psycopg import Cursor

from dbrewinder.dbcursor_interface import DBCursorInterface


class DBCursor(DBCursorInterface):
    def __init__(self, cursor: Cursor):
        self.cursor = cursor
