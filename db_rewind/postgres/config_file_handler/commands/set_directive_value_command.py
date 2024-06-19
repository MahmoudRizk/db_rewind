from typing import Optional

from db_rewind.postgres.config_file_handler.commands.abstract_command import AbstractCommand
from db_rewind.postgres.config_file_handler.config_line import ConfigLine


class SetDirectiveValueCommand(AbstractCommand):
    def __init__(self, directive_name: str, directive_value: any, use_single_quotation: bool = False):
        self.directive_name = directive_name
        self.directive_value = directive_value
        self.use_single_quotation = use_single_quotation

    def execute(self, line: Optional[ConfigLine] = None) -> ConfigLine:
        if not line:
            _line = f"{self.directive_name} = " + (
                f"'{self.directive_value}'" if self.use_single_quotation else f"{self.directive_value}")
            return ConfigLine(line=_line)

        return line.set_directive_value(self.directive_value, self.use_single_quotation)

    def get_directive_name(self):
        return self.directive_name
