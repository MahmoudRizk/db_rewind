from typing import Optional

from vendors.postgres import from_env
from vendors.postgres.os_handler.os_command_handler import OsCommandHandler
from vendors.postgres.os_handler.os_response_dto import OsResponseDTO
from vendors.postgres.procedures.base_procedure import BaseProcedure


class CreateDBBaseBackup(BaseProcedure):
    def execute_as_user(self) -> Optional[str]:
        return from_env('DB_REWINDER_HOST_POSTGRES_USER')

    def _execute(self) -> OsResponseDTO:
        return self._SetDBInBackupMode().next(
            self._BackupDatabase().next(
                self._StopDBBackupMode()
            )
        ).execute()

    class _SetDBInBackupMode(BaseProcedure):
        def _execute(self) -> OsResponseDTO:
            # Set database in backup mode first using.
            command = "psql -c \"SELECT pg_start_backup('label');\""
            self.print_info('Running pg_start_backup.')
            self.print_info(f"using command: {command}")
            return OsCommandHandler.execute(command)

    class _BackupDatabase(BaseProcedure):
        def _execute(self) -> OsResponseDTO:
            base_backup_dir = from_env("DB_REWINDER_POSTGRES_BASE_BACKUP_DIR")
            main_db_dir = from_env("DB_REWINDER_POSTGRES_DATA_DIR")

            backup_file_name = 'db_rewinder.tar.gz'

            # Backing up database.
            command = f"tar -czf {base_backup_dir}/{backup_file_name} -C {main_db_dir} --exclude=pg_wal ."
            self.print_info('creating db backup.')
            self.print_info(f"using: {command}")
            return OsCommandHandler.execute(command)

    class _StopDBBackupMode(BaseProcedure):
        def _execute(self) -> OsResponseDTO:
            # Stop database backup mode.
            command = 'psql -c "SELECT pg_stop_backup();"'
            self.print_info('Running pg_stop_backup.')
            self.print_info(f"using command: {command}")
            return OsCommandHandler.execute(command)
