from typing import Optional, List

from .commands.abstract_command import AbstractCommand
from .config_line import ConfigLine
from .file_io import FileIO


class FileHandler:
    def __init__(self, file_io: FileIO):
        self.file_io = file_io

        self.lines = self.file_io.read_file()
        self.commands = []

    def apply_command(self, command: AbstractCommand) -> None:
        self.commands.append(command)

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
