from typing import Optional

from vendors.postgres import from_env
from vendors.postgres.config_file_handler.file_handler import FileHandler
from vendors.postgres.os_handler.os_response_dto import OsResponseDTO
from vendors.postgres.procedures.base_procedure import BaseProcedure


class ConfigFileSetup(BaseProcedure):
    def execute_as_user(self) -> Optional[str]:
        return from_env('DB_REWINDER_HOST_POSTGRES_USER')

    def _execute(self) -> OsResponseDTO:
        print('Configuring postgres configuration file.')
        print(f"Postgres Config File: {self.file_path}")

        print('Editing postgres config file.')
        self.enable_and_set_wal_level_to_archive()
        self.enable_and_set_archive_mode_to_on()
        self.enable_and_set_archive_command()
        self.enable_and_set_restore_command()

        self.config_file.save()

        return OsResponseDTO(exit_code=0)

    def __init__(self,
                 file_path: str = from_env('DB_REWINDER_POSTGRES_CONFIG_FILE_PATH'),
                 archive_command: str = from_env('DB_REWINDER_POSTGRES_ARCHIVE_COMMAND'),
                 restore_command: str = from_env('DB_REWINDER_POSTGRES_RESTORE_COMMAND')):
        super().__init__()

        self.file_path = file_path
        self.config_file = FileHandler(file_path=self.file_path)
        self.archive_command = archive_command
        self.restore_command = restore_command

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
