from typing import Optional, List

from vendors.postgres.config_file_handler.config_line import ConfigLine
from vendors.postgres.config_file_handler.file_handler_commands import EnableDirectiveCommand, DisableDirectiveCommand, \
    SetDirectiveValueCommand


class FileHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path

        self.lines = self._read_file()
        self.commands = []

    def enable_directive(self, name: str) -> "FileHandler":
        self.commands.append(
            EnableDirectiveCommand(directive_name=name)
        )
        return self

    def disable_directive(self, name: str) -> "FileHandler":
        self.commands.append(
            DisableDirectiveCommand(directive_name=name)
        )
        return self

    def set_directive_value(self, name: str, value: any, use_single_quotation=False) -> "FileHandler":
        self.commands.append(
            SetDirectiveValueCommand(directive_name=name, directive_value=value,
                                     use_single_quotation=use_single_quotation)
        )
        return self

    def save(self) -> None:
        for command in self.commands:
            directive_name = command.get_directive_name()

            line = self._get_line_with_directive_name(directive_name)

            is_new = True if not line else False
            line = command.execute(line=line)

            if is_new:
                self.lines.append(line)

        self._write_file()

    def _get_line_with_directive_name(self, name: str) -> Optional[ConfigLine]:
        for line in self.lines:
            if line.has_directive(name=name):
                return line
        return None

    def _read_file(self) -> List[ConfigLine]:
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            return [ConfigLine(line) for line in lines]

    def _write_file(self) -> None:
        with open(self.file_path, 'w') as file:
            lines = [line.get() for line in self.lines]
            file.writelines(lines)