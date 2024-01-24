import abc
from abc import abstractmethod


class AbstractSetup(metaclass=abc.ABCMeta):

    @abstractmethod
    def create_logs_table(self):
        pass

    @abstractmethod
    def create_trigger_function(self):
        pass

    @abstractmethod
    def register_table_to_trigger(self, table_name: str):
        pass

    @abstractmethod
    def register_all_tables_to_trigger(self):
        pass

