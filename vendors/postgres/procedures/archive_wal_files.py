from typing import Optional

from vendors.postgres import from_env
from vendors.postgres.os_handler.os_command_handler import OsCommandHandler
from vendors.postgres.os_handler.os_response_dto import OsResponseDTO

from vendors.postgres.procedures.base_procedure import BaseProcedure


class ArchiveWalFiles(BaseProcedure):
    def execute_as_user(self) -> Optional[str]:
        return from_env('DB_REWINDER_HOST_POSTGRES_USER')

    def can_user_handle_error_manually(self) -> bool:
        return True

    def _execute(self) -> OsResponseDTO:
        command = 'psql -c "select pg_switch_wal();"'
        self.print_info('archiving wal files, using pg_switch_wal()')
        self.print_info(f'executing: {command}')

        return OsCommandHandler.execute(command)
