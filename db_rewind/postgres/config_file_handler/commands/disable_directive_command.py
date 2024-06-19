from typing import Optional, List

from db_rewind.postgres.config_file_handler.commands.abstract_command import AbstractCommand, \
    get_line_with_directive_name
from db_rewind.postgres.config_file_handler.config_line import ConfigLine


class DisableDirectiveCommand(AbstractCommand):
    def __init__(self, directive_name: str):
        self.directive_name = directive_name

    def execute(self, file_lines: List[ConfigLine]) -> None:
        line = get_line_with_directive_name(self.directive_name, file_lines)
        if line:
            line.disable_directive()
