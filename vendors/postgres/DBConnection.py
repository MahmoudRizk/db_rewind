import psycopg
from psycopg import Connection

from dbrewinder import DBConnectionInterface
from vendors.postgres.DBCursor import DBCursor


class DBConnection(DBConnectionInterface):

    @staticmethod
    def get_connection(
            database_name: str,
            username: str,
            password: str,
            host: str,
            port: str
    ):
        return DBConnection(
            database_name=database_name,
            username=username,
            password=password,
            host=host,
            port=port
        )

    def __init__(self, database_name: str, username: str, password: str, host: str, port: str):
        self.port = port
        self.host = host
        self.password = password
        self.username = username
        self.database_name = database_name

        self.uri: str = self._construct_database_uri()
        self.connection: Connection = psycopg.connect(self.uri)

    def cursor(self):
        return DBCursor(self.connection.cursor())

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()

    def _construct_database_uri(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}"
