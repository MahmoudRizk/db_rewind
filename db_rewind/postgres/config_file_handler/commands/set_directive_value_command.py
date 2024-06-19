from typing import List

from db_rewind.postgres.config_file_handler.commands.abstract_command import AbstractCommand, \
    get_line_with_directive_name
from db_rewind.postgres.config_file_handler.config_line import ConfigLine


class SetDirectiveValueCommand(AbstractCommand):
    def __init__(self, directive_name: str, directive_value: any, use_single_quotation: bool = False):
        self.directive_name = directive_name
        self.directive_value = directive_value
        self.use_single_quotation = use_single_quotation

    def execute(self, file_lines: List[ConfigLine]) -> None:
        line = get_line_with_directive_name(self.directive_name, file_lines)
        if line:
            line.set_directive_value(self.directive_value, self.use_single_quotation)
        else:
            self.add_new_line_to_file_lines(file_lines)

    def add_new_line_to_file_lines(self, file_lines: List[ConfigLine]) -> None:
        # Add line break to last line.
        if file_lines[-1]:
            file_lines[-1].add_line_break()

        file_lines.append(self.construct_new_config_line())

    def construct_new_config_line(self) -> ConfigLine:
        return ConfigLine(
            f"{self.directive_name} = " + (
                f"'{self.directive_value}'" if self.use_single_quotation else f"{self.directive_value}")
        )
