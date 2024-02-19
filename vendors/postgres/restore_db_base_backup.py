from vendors.postgres import from_env
from vendors.postgres.os_handler.os_command_handler import OsCommandHandler
from vendors.postgres.os_handler.os_new_process_handler import OsNewProcessHandler
from vendors.postgres.os_handler.os_response_dto import OsResponseDTO


class RestoreDBBaseBackup:
    @staticmethod
    @OsNewProcessHandler.in_new_process(as_user=from_env('DB_REWINDER_HOST_POSTGRES_USER'))
    def execute() -> OsResponseDTO:
        # if not success, return and skip executing next procedures.
        res = RestoreDBBaseBackup.restore_backup()
        if not res.is_success():
            return res

        return RestoreDBBaseBackup.create_missing_wal_directory()

    @staticmethod
    def restore_backup() -> OsResponseDTO:
        base_backup_dir = from_env("DB_REWINDER_POSTGRES_BASE_BACKUP_DIR")
        main_db_dir = from_env("DB_REWINDER_POSTGRES_DATA_DIR")

        # "tar xvfz /var/lib/postgresql/base_backup_12/base.tar -C ./"

        # TODO: solve hard coded file name.
        backup_file_name = 'db_rewinder.tar.gz'

        command = f"tar xfz {base_backup_dir}/{backup_file_name} -C {main_db_dir}"

        return OsCommandHandler.execute(command)

    @staticmethod
    def create_missing_wal_directory() -> OsResponseDTO:
        main_db_dir = from_env("DB_REWINDER_POSTGRES_DATA_DIR")

        command = f"mkdir {main_db_dir}/pg_wal"
        print("Creating missing pg_wal directory")
        print(f"using command: {command}")

        return OsCommandHandler.execute(command)
