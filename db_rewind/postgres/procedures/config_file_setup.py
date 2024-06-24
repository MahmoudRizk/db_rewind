from typing import Optional

from db_rewind.postgres import from_env
from db_rewind.postgres.config_file_handler.commands.set_directive_value_command import SetDirectiveValueCommand
from db_rewind.postgres.config_file_handler.file_handler import FileHandler
from db_rewind.postgres.config_file_handler.file_io import FileIO
from db_rewind.postgres.os_handler.os_response_dto import OsResponseDTO
from db_rewind.postgres.procedures.base_procedure import BaseProcedure


class ConfigFileSetup(BaseProcedure):
    def execute_as_user(self) -> Optional[str]:
        return from_env('DB_REWINDER_HOST_POSTGRES_USER')

    def _execute(self) -> OsResponseDTO:
        self.print_info('Configuring postgres configuration file.')
        self.print_info(f"Postgres Config File: {self.file_path}")

        self.print_info('Editing postgres config file.')
        self.enable_and_set_wal_level_to_archive()
        self.enable_and_set_archive_mode_to_on()
        self.enable_and_set_archive_command()
        self.enable_and_set_restore_command()

        self.config_file.save()

        return OsResponseDTO(exit_code=0)

    def __init__(self,
                 file_path: str = from_env('DB_REWINDER_POSTGRES_CONFIG_FILE_PATH'),
                 archive_command: str = from_env('DB_REWINDER_POSTGRES_ARCHIVE_COMMAND'),
                 restore_command: str = from_env('DB_REWINDER_POSTGRES_RESTORE_COMMAND'),
                 wal_archive_dir: str = from_env('DB_REWINDER_POSTGRES_WAL_BACKUP_DIR')):
        super().__init__()

        self.file_path = file_path

        file_io = FileIO(file_path)
        self.config_file = FileHandler(file_io=file_io)

        self.archive_command = archive_command.format(DB_REWINDER_POSTGRES_WAL_BACKUP_DIR=wal_archive_dir)
        self.restore_command = restore_command.format(DB_REWINDER_POSTGRES_WAL_BACKUP_DIR=wal_archive_dir)

    def enable_and_set_wal_level_to_archive(self) -> None:
        self.print_info('enable wal archive.')
        self.config_file.apply_command(SetDirectiveValueCommand('wal_level', 'archive'))

    def enable_and_set_archive_mode_to_on(self) -> None:
        self.print_info('set archive mode to on.')
        self.config_file.apply_command(SetDirectiveValueCommand('archive_mode', 'on'))

    def enable_and_set_archive_command(self) -> None:
        self.print_info('set archive command.')
        self.config_file.apply_command(SetDirectiveValueCommand('archive_command', self.archive_command, True))

    def enable_and_set_restore_command(self) -> None:
        self.print_info('set restore command.')
        self.config_file.apply_command(SetDirectiveValueCommand('restore_command', self.restore_command, True))
