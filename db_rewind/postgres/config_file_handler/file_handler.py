from typing import Optional, List

from .commands.disable_directive_command import DisableDirectiveCommand
from .commands.enable_directive_command import EnableDirectiveCommand
from .commands.set_directive_value_command import SetDirectiveValueCommand
from .config_line import ConfigLine
from .file_io import FileIO


class FileHandler:
    def __init__(self, file_io: FileIO):
        self.file_io = file_io

        self.lines = self.file_io.read_file()
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

    def save(self, in_memory: bool = False) -> List[str]:
        for command in self.commands:
            directive_name = command.get_directive_name()

            line = self._get_line_with_directive_name(directive_name)

            is_new = True if not line else False
            line = command.execute(line=line)

            if is_new and line.get() != '':
                self.lines[-1] and self.lines[-1].add_line_break()
                self.lines.append(line)

        return self.file_io.write_file(self.lines, in_memory)

    def _get_line_with_directive_name(self, name: str) -> Optional[ConfigLine]:
        for line in self.lines:
            if line.has_directive(name=name):
                return line
        return None
