from vendors.postgres import from_env
from vendors.postgres.os_handler.os_command_handler import OsCommandHandler
from vendors.postgres.os_handler.os_new_process_handler import OsNewProcessHandler
from vendors.postgres.os_handler.os_response_dto import OsResponseDTO


class DBServerManager:
    @staticmethod
    @OsNewProcessHandler.in_new_process(as_user=from_env('DB_REWINDER_HOST_ROOT_USER'))
    def execute(command: str) -> OsResponseDTO:
        sys_command = f"systemctl {command} postgresql.service"
        print(f"{command} postgres server using systemctl: {sys_command}")

        return OsCommandHandler.execute(sys_command)
