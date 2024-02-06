import abc
from abc import abstractmethod


class Column(metaclass=abc.ABCMeta):
    @abstractmethod
    def random_value_generator(self) -> str:
        pass

    @abstractmethod
    def get_column_type(self) -> str:
        pass