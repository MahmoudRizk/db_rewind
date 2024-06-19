from typing import Optional

from db_rewind.postgres.config_file_handler.commands.abstract_command import AbstractCommand
from db_rewind.postgres.config_file_handler.config_line import ConfigLine


class DisableDirectiveCommand(AbstractCommand):
    def __init__(self, directive_name: str):
        self.directive_name = directive_name

    def execute(self, line: Optional[ConfigLine] = None) -> ConfigLine:
        if not line:
            # Return Empty Line.
            return ConfigLine(line="")

        return line.disable_directive()

    def get_directive_name(self):
        return self.directive_name
