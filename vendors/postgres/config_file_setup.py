from vendors.postgres.config_file_handler.file_handler import FileHandler


class ConfigFileSetup:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def execute(self):
        config_file = FileHandler(file_path=self.file_path)

        config_file.set_directive_value('wal_level', 'archive')
        config_file.set_directive_value('archive_mode', 'on')

        archive_command = 'test ! -f /var/lib/postgresql/pg_log_archive/%f && cp %p /var/lib/postgresql/pg_log_archive/%f'
        config_file.set_directive_value('archive_command', archive_command, True)

        config_file.save()
