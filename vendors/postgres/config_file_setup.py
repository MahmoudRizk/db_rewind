import os

from vendors.postgres import switch_user
from .config_file_handler.file_handler import FileHandler


class ConfigFileSetup:
    def __init__(self, file_path: str, archive_command: str, restore_command: str):
        self.file_path = file_path
        self.config_file = FileHandler(file_path=self.file_path)
        self.archive_command = archive_command
        self.restore_command = restore_command

    def execute(self) -> None:
        print('Editing postgres config file.')
        self.enable_and_set_wal_level_to_archive()
        self.enable_and_set_archive_mode_to_on()
        self.enable_and_set_archive_command()
        self.enable_and_set_restore_command()

        self.config_file.save()

    def enable_and_set_wal_level_to_archive(self) -> None:
        print('enable wal archive.')
        self.config_file.set_directive_value(name='wal_level', value='archive')

    def enable_and_set_archive_mode_to_on(self) -> None:
        print('set archive mode to on.')
        self.config_file.set_directive_value('archive_mode', 'on')

    def enable_and_set_archive_command(self) -> None:
        print('set archive command.')
        self.config_file.set_directive_value('archive_command', self.archive_command, True)

    def enable_and_set_restore_command(self) -> None:
        print('set restore command.')
        self.config_file.set_directive_value('restore_command', self.restore_command, True)


if __name__ == '__main__':
    user_name = os.environ['DB_REWINDER_HOST_POSTGRES_USER']
    switch_user(user_name=user_name)

    print('Configuring postgres configuration file.')
    file_path = os.environ['DB_REWINDER_POSTGRES_CONFIG_FILE_PATH']
    print(f"Postgres Config File: {file_path}")

    archive_command = os.environ['DB_REWINDER_POSTGRES_ARCHIVE_COMMAND']
    restore_command = os.environ['DB_REWINDER_POSTGRES_RESTORE_COMMAND']

    config_file_setup = ConfigFileSetup(file_path=file_path, archive_command=archive_command,
                                        restore_command=restore_command)
    config_file_setup.execute()
