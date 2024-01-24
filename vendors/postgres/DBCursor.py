from dbrewinder import DBCursorInterface
from psycopg import Cursor


class DBCursor(DBCursorInterface):
    def __init__(self, cursor: Cursor):
        self.cursor = cursor
