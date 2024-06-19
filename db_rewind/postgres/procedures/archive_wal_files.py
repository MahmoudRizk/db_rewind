from typing import Optional

from db_rewind.postgres import from_env
from db_rewind.postgres.os_handler.os_command_handler import OsCommandHandler
from db_rewind.postgres.os_handler.os_response_dto import OsResponseDTO
from db_rewind.postgres.procedures.base_procedure import BaseProcedure


class ArchiveWalFiles(BaseProcedure):
    def execute_as_user(self) -> Optional[str]:
        return from_env('DB_REWINDER_HOST_POSTGRES_USER')

    def _execute(self) -> OsResponseDTO:
        command = 'psql -c "select pg_switch_wal();"'
        self.print_info('archiving wal files, using pg_switch_wal()')
        self.print_info(f'executing: {command}')

        return OsCommandHandler.execute(command)
