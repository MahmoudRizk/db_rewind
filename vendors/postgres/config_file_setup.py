from vendors.postgres.config_file_handler.file_handler import FileHandler


class ConfigFileSetup:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.config_file = FileHandler(file_path=self.file_path)

    def execute(self):
        self.enable_and_set_wal_level_to_archive()
        self.enable_and_set_archive_mode_to_on()
        self.enable_and_set_archive_command()

        self.config_file.save()

    def enable_and_set_wal_level_to_archive(self) -> None:
        self.config_file.set_directive_value(name='wal_level', value='archive')

    def enable_and_set_archive_mode_to_on(self) -> None:
        self.config_file.set_directive_value('archive_mode', 'on')

    def enable_and_set_archive_command(self) -> None:
        archive_command = 'test ! -f /var/lib/postgresql/pg_log_archive/%f && cp %p /var/lib/postgresql/pg_log_archive/%f'
        self.config_file.set_directive_value('archive_command', archive_command, True)
