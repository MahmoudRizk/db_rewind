from pathlib import Path
from typing import List

from db_rewind.postgres.config_file_handler.config_line import ConfigLine


class FileIO:
    def __init__(self, file_path: str | Path):
        self.file_path = file_path

    def read_file(self) -> List[ConfigLine]:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return [ConfigLine(line) for line in lines]

    def write_file(self, lines: List[ConfigLine], in_memory: bool = False) -> List[str]:
        lines = [f"{line.get()}" for line in lines]

        if not in_memory:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.writelines(lines)

        return lines
