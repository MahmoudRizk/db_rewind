from typing import Optional

from db_rewind.postgres import from_env
from db_rewind.postgres.os_handler.os_command_handler import OsCommandHandler
from db_rewind.postgres.os_handler.os_response_dto import OsResponseDTO
from db_rewind.postgres.procedures.base_procedure import BaseProcedure


class DBServerManager(BaseProcedure):
    def __init__(self, command: str):
        super().__init__()
        self.command = command

    @staticmethod
    def stop() -> "DBServerManager":
        return DBServerManager(command='stop')

    @staticmethod
    def start() -> "DBServerManager":
        return DBServerManager(command='start')

    @staticmethod
    def restart() -> "DBServerManager":
        return DBServerManager(command='restart')

    def execute_as_user(self) -> Optional[str]:
        return from_env('DB_REWINDER_HOST_ROOT_USER')

    def _execute(self) -> OsResponseDTO:
        sys_command = f"systemctl {self.command} postgresql@12-main.service"
        self.print_info(f"{self.command} postgres server using systemctl: {sys_command}")

        return OsCommandHandler.execute(sys_command)
