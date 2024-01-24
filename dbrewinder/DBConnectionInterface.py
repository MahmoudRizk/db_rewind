import abc
from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from DBCursorInterface import DBCursorInterface


class DBConnectionInterface(metaclass=abc.ABCMeta):
    @staticmethod
    @abstractmethod
    def get_connection(
            database_name: str,
            username: str,
            password: str,
            host: str,
            port: str
    ) -> "DBConnectionInterface":
        pass

    @abstractmethod
    def cursor(self) -> DBCursorInterface:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
