from typing import Optional

from vendors.postgres import from_env
from vendors.postgres.os_handler.os_command_handler import OsCommandHandler
from vendors.postgres.os_handler.os_response_dto import OsResponseDTO

from vendors.postgres.procedures.base_procedure import BaseProcedure


class ArchiveWalFiles(BaseProcedure):

    def execute_as_user(self) -> Optional[str]:
        return from_env('DB_REWINDER_HOST_POSTGRES_USER')

    def _execute(self) -> OsResponseDTO:
        command = 'psql -c "select pg_switch_wal();"'
        print('archiving wal files, using pg_switch_wal()')
        print(f'executing: {command}')

        return OsCommandHandler.execute(command)
