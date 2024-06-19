import abc
from typing import Optional, List

from db_rewind.postgres.config_file_handler.config_line import ConfigLine


class AbstractCommand(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, file_lines: List[ConfigLine]) -> None:
        pass


def get_line_with_directive_name(name: str, file_lines: List[ConfigLine]) -> Optional[ConfigLine]:
    for line in file_lines:
        if line.has_directive(name=name):
            return line
    return None
