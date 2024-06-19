import abc
from typing import Optional

from db_rewind.postgres.config_file_handler.config_line import ConfigLine


class AbstractCommand(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, line: Optional[ConfigLine] = None) -> ConfigLine:
        pass

    @abc.abstractmethod
    def get_directive_name(self):
        pass
