from typing import Optional

from vendors.postgres import from_env
from vendors.postgres.os_handler.os_command_handler import OsCommandHandler
from vendors.postgres.os_handler.os_response_dto import OsResponseDTO
from vendors.postgres.procedures.base_procedure import BaseProcedure


class RestoreDBBaseBackup(BaseProcedure):
    def execute_as_user(self) -> Optional[str]:
        return from_env('DB_REWINDER_HOST_POSTGRES_USER')

    def _execute(self) -> OsResponseDTO:
        return self._RestoreBackup().next(
            self._CreateMissingWalDirectory()
        ).execute()

    class _RestoreBackup(BaseProcedure):
        def _execute(self) -> OsResponseDTO:
            base_backup_dir = from_env("DB_REWINDER_POSTGRES_BASE_BACKUP_DIR")
            main_db_dir = from_env("DB_REWINDER_POSTGRES_DATA_DIR")

            # "tar xvfz /var/lib/postgresql/base_backup_12/base.tar -C ./"

            # TODO: solve hard coded file name.
            backup_file_name = 'db_rewinder.tar.gz'

            command = f"tar xfz {base_backup_dir}/{backup_file_name} -C {main_db_dir}"

            return OsCommandHandler.execute(command)

    class _CreateMissingWalDirectory(BaseProcedure):
        def _execute(self) -> OsResponseDTO:
            main_db_dir = from_env("DB_REWINDER_POSTGRES_DATA_DIR")

            command = f"mkdir {main_db_dir}/pg_wal"
            self.print_info("Creating missing pg_wal directory")
            self.print_info(f"using command: {command}")

            return OsCommandHandler.execute(command)
