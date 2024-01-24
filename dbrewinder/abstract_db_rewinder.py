import abc
from abc import abstractmethod
from enum import Enum
from typing import List, Optional
from datetime import datetime


class LogEvent(Enum):
    UPDATE = 'UPDATE'
    INSERT = 'INSERT'
    DELETE = 'DELETE'


class Log:
    def __init__(self,
                 id: int,
                 timestamp: datetime,
                 table_name: str,
                 operation: LogEvent,
                 new_val: Optional[dict],
                 old_val: Optional[dict]):
        self.id = id
        self.timestamp = timestamp
        self.table_name = table_name
        self.operation = operation
        self.new_val = new_val
        self.old_val = old_val


class AbstractDBRewinder(metaclass=abc.ABCMeta):
    def rewind(self):
        self.disable_all_db_triggers()

        tables_history_events: List[Log] = self.get_logs()

        for row in tables_history_events:
            match row.operation:
                case LogEvent.UPDATE:
                    self.update_from_json(row.table_name, row.old_val)
                case LogEvent.INSERT:
                    self.delete_from_json(row.table_name, row.new_val)
                case LogEvent.DELETE:
                    self.insert_from_json(row.table_name, row.old_val)

        self.flush_logs()
        self.enable_all_db_triggers()

    @abstractmethod
    def disable_all_db_triggers(self) -> None:
        pass

    @abstractmethod
    def enable_all_db_triggers(self) -> None:
        pass

    @abstractmethod
    def get_logs(self) -> List[Log]:
        pass

    @abstractmethod
    def update_from_json(self, table_name: str, json_value: dict) -> None:
        pass

    @abstractmethod
    def delete_from_json(self, table_name: str, json_value: dict) -> None:
        pass

    @abstractmethod
    def insert_from_json(self, table_name: str, json_value: dict) -> None:
        pass

    @abstractmethod
    def flush_logs(self) -> None:
        pass
