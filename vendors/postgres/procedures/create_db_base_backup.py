from vendors.postgres import from_env
from vendors.postgres.os_handler.os_command_handler import OsCommandHandler
from vendors.postgres.os_handler.os_new_process_handler import OsNewProcessHandler
from vendors.postgres.os_handler.os_response_dto import OsResponseDTO
from vendors.postgres.procedures.base_procedure import BaseProcedure


class CreateDBBaseBackup(BaseProcedure):

    @OsNewProcessHandler.in_new_process(as_user=from_env('DB_REWINDER_HOST_POSTGRES_USER'))
    def _execute(self) -> OsResponseDTO:
        # Return failed procedure and skip executing others.

        res = CreateDBBaseBackup.set_db_in_backup_mode()
        if not res.is_success():
            return res

        res = CreateDBBaseBackup.backup_database()
        if not res.is_success():
            return res

        return CreateDBBaseBackup.stop_db_backup_mode()

    @staticmethod
    def set_db_in_backup_mode() -> OsResponseDTO:
        # Set database in backup mode first using.
        command = "psql -c \"SELECT pg_start_backup('label');\""
        print('Running pg_start_backup.')
        print(f"using command: {command}")
        return OsCommandHandler.execute(command)

    @staticmethod
    def backup_database() -> OsResponseDTO:
        base_backup_dir = from_env("DB_REWINDER_POSTGRES_BASE_BACKUP_DIR")
        main_db_dir = from_env("DB_REWINDER_POSTGRES_DATA_DIR")

        backup_file_name = 'db_rewinder.tar.gz'

        # Backing up database.
        command = f"tar -czf {base_backup_dir}/{backup_file_name} -C {main_db_dir} --exclude=pg_wal ."
        print('creating db backup.')
        print(f"using: {command}")
        return OsCommandHandler.execute(command)

    @staticmethod
    def stop_db_backup_mode() -> OsResponseDTO:
        # Stop database backup mode.
        command = 'psql -c "SELECT pg_stop_backup();"'
        print('Running pg_stop_backup.')
        print(f"using command: {command}")
        return OsCommandHandler.execute(command)
