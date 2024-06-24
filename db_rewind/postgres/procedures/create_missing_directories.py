import os.path
from typing import Optional

from db_rewind.postgres import from_env
from db_rewind.postgres.os_handler.os_command_handler import OsCommandHandler
from db_rewind.postgres.os_handler.os_response_dto import OsResponseDTO
from db_rewind.postgres.procedures.base_procedure import BaseProcedure


class CreateMissingDirectories(BaseProcedure):
    def __init__(self, dir_path: str, **kwargs):
        super().__init__(**kwargs)

        self.dir_path = dir_path

    def execute_as_user(self) -> Optional[str]:
        return from_env('DB_REWINDER_HOST_POSTGRES_USER')

    def _execute(self) -> OsResponseDTO:
        if not os.path.exists(self.dir_path):
            command = f"mkdir {self.dir_path}"
            self.print_info(f"Creating missing directory using command: {command}")
            return OsCommandHandler.execute(command)
        else:
            self.print_info(f"Dir path already exists {self.dir_path}")
            return OsResponseDTO(exit_code=0)
