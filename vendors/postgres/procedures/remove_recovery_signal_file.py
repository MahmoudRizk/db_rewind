from typing import Optional
from pathlib import Path

from vendors.postgres import from_env
from vendors.postgres.os_handler.os_command_handler import OsCommandHandler
from vendors.postgres.os_handler.os_response_dto import OsResponseDTO
from vendors.postgres.procedures.base_procedure import BaseProcedure


class RemoveRecoverySignalFile(BaseProcedure):
    def execute_as_user(self) -> Optional[str]:
        return from_env('DB_REWINDER_HOST_POSTGRES_USER')
    
    def _execute(self) -> OsResponseDTO:
        main_db_dir = from_env('DB_REWINDER_POSTGRES_DATA_DIR')

        file_path = f"{main_db_dir}/recovery.signal"
        
        if not self._file_exists(file_path):
            self.print_info("Skipping removing recovery.signal file. File doesn't exist")
            return OsResponseDTO(0, b'', b'')

        command = f"rm {file_path}"

        self.print_info("Removing recovery signal conf file")
        self.print_info(f"Using command: {command}")

        return OsCommandHandler.execute(command)

    def _file_exists(self, file_path: str):
        if Path(file_path).is_file():
            return True
        return False