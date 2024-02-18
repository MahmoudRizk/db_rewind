from vendors.postgres import from_env
from vendors.postgres.os_handler.os_command_handler import OsCommandHandler
from vendors.postgres.os_handler.os_new_process_handler import OsNewProcessHandler


class CreateRecoverySignalFile:
    @staticmethod
    @OsNewProcessHandler.in_new_process(as_user=from_env('DB_REWINDER_HOST_POSTGRES_USER'))
    def execute():
        main_db_dir = from_env("DB_REWINDER_POSTGRES_DATA_DIR")

        command = f"touch {main_db_dir}/recovery.signal"

        print('Creating recovery signal conf file')
        print(f"Using command: {command}")

        return OsCommandHandler.execute(command)
