from typing import Optional

from vendors.postgres import from_env
from vendors.postgres.os_handler.os_command_handler import OsCommandHandler
from vendors.postgres.os_handler.os_response_dto import OsResponseDTO
from vendors.postgres.procedures.base_procedure import BaseProcedure


class DBServerManager(BaseProcedure):
    def __init__(self, command: str):
        super().__init__()
        self.command = command

    def execute_as_user(self) -> Optional[str]:
        return from_env('DB_REWINDER_HOST_ROOT_USER')

    def _execute(self) -> OsResponseDTO:
        sys_command = f"systemctl {self.command} postgresql.service"
        print(f"{self.command} postgres server using systemctl: {sys_command}")

        return OsCommandHandler.execute(sys_command)
