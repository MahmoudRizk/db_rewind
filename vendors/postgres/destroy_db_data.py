from vendors.postgres import from_env
from vendors.postgres.os_handler.os_command_handler import OsCommandHandler
from vendors.postgres.os_handler.os_new_process_handler import OsNewProcessHandler
from vendors.postgres.os_handler.os_response_dto import OsResponseDTO


class DestroyDBData:
    @staticmethod
    @OsNewProcessHandler.in_new_process(as_user=from_env('DB_REWINDER_HOST_POSTGRES_USER'))
    def execute() -> OsResponseDTO:
        main_db_dir = from_env("DB_REWINDER_POSTGRES_DATA_DIR")

        command = f"rm -r {main_db_dir}/*"

        print("Destroying database files.")
        print(f"using command: {command}")

        return OsCommandHandler.execute(command)
