from typing import Optional, List

config_file_path = '/home/mahmoudrizk/db_time_travel/vendors/postgres/postgresql.conf'
db_data_directory = ''


class Line:
    def __init__(self, line: str):
        self.original_line = line
        self.line = line

    def get(self) -> str:
        return self.line

    def get_directive_name(self) -> str:
        split_line = self.line.split()
        directive_name = split_line and split_line[0] or ''
        return directive_name[1:] if directive_name.startswith('#') else directive_name

    def enable_directive(self) -> "Line":
        self.line = self.line[1:] if self.line.startswith('#') else self.line
        return self

    def disable_directive(self) -> "Line":
        self.line = self.line if self.line.startswith('#') else '#' + self.line
        return self

    def set_directive_value(self, value: any, use_single_quotation: bool) -> "Line":
        directive_name: str = self.get_directive_name()
        if directive_name:
            _line = f"{directive_name} = " + (f"'{value}'" if use_single_quotation else f"{value}")
            self.line = _line + ' ' + self._get_line_comment()
        return self

    def has_directive(self, name: str) -> bool:
        return self.get_directive_name() == name

    def _get_line_comment(self) -> str:
        # Finds second occurrence of '#', then return sub string starting from its occurrence.
        return self.line[self.line.find('#', 1):]


class EnableDirectiveCommand:
    def __init__(self, directive_name: str):
        self.directive_name = directive_name

    def execute(self, line: Optional[Line] = None) -> Line:
        if not line:
            # Return Empty Line.
            return Line(line="")

        return line.enable_directive()

    def get_directive_name(self):
        return self.directive_name


class DisableDirectiveCommand:
    def __init__(self, directive_name: str):
        self.directive_name = directive_name

    def execute(self, line: Optional[Line] = None) -> Line:
        if not line:
            # Return Empty Line.
            return Line(line="")

        return line.disable_directive()

    def get_directive_name(self):
        return self.directive_name


class SetDirectiveValueCommand:
    def __init__(self, directive_name: str, directive_value: any, use_single_quotation: bool = False):
        self.directive_name = directive_name
        self.directive_value = directive_value
        self.use_single_quotation = use_single_quotation

    def execute(self, line: Optional[Line] = None) -> Line:
        if not line:
            _line = f"{self.directive_name} = " + (
                f"'{self.directive_value}'" if self.use_single_quotation else f"{self.directive_value}")
            return Line(line=_line)

        return line.set_directive_value(self.directive_value, self.use_single_quotation)

    def get_directive_name(self):
        return self.directive_name


class ConfigFile:
    def __init__(self, file_path: str):
        self.file_path = file_path

        self.lines = self._read_file()
        self.commands = []

    def enable_directive(self, name: str) -> "ConfigFile":
        self.commands.append(
            EnableDirectiveCommand(directive_name=name)
        )
        return self

    def disable_directive(self, name: str) -> "ConfigFile":
        self.commands.append(
            DisableDirectiveCommand(directive_name=name)
        )
        return self

    def set_directive_value(self, name: str, value: any, use_single_quotation=False) -> "ConfigFile":
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

    def _get_line_with_directive_name(self, name: str) -> Optional[Line]:
        for line in self.lines:
            if line.has_directive(name=name):
                return line
        return None

    def _read_file(self) -> List[Line]:
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            return [Line(line) for line in lines]

    def _write_file(self) -> None:
        with open(self.file_path, 'w') as file:
            lines = [line.get() for line in self.lines]
            file.writelines(lines)


if __name__ == '__main__':
    config_file = ConfigFile(file_path=config_file_path)

    config_file.set_directive_value('wal_level', 'archive')
    config_file.set_directive_value('archive_mode', 'on')

    archive_command = 'test ! -f /var/lib/postgresql/pg_log_archive/%f && cp %p /var/lib/postgresql/pg_log_archive/%f'
    config_file.set_directive_value('archive_command', archive_command, True)

    config_file.save()
