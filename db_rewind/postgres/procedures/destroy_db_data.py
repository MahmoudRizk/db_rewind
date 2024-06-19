from typing import Optional

from db_rewind.postgres import from_env
from db_rewind.postgres.os_handler.os_command_handler import OsCommandHandler
from db_rewind.postgres.os_handler.os_response_dto import OsResponseDTO
from db_rewind.postgres.procedures.base_procedure import BaseProcedure


class DestroyDBData(BaseProcedure):
    def execute_as_user(self) -> Optional[str]:
        return from_env('DB_REWINDER_HOST_POSTGRES_USER')

    def _execute(self) -> OsResponseDTO:
        main_db_dir = from_env("DB_REWINDER_POSTGRES_DATA_DIR")

        command = f"rm -r {main_db_dir}/*"

        self.print_info("Destroying database files.")
        self.print_info(f"using command: {command}")

        return OsCommandHandler.execute(command)
