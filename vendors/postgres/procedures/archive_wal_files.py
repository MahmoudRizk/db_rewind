from vendors.postgres import from_env
from vendors.postgres.os_handler.os_command_handler import OsCommandHandler
from vendors.postgres.os_handler.os_response_dto import OsResponseDTO

from vendors.postgres.os_handler.os_new_process_handler import OsNewProcessHandler
from vendors.postgres.procedures.base_procedure import BaseProcedure


class ArchiveWalFiles(BaseProcedure):

    @OsNewProcessHandler.in_new_process(as_user=from_env('DB_REWINDER_HOST_POSTGRES_USER'))
    def _execute(self) -> OsResponseDTO:
        command = 'psql -c "select pg_switch_wal();"'
        print('archiving wal files, using pg_switch_wal()')
        print(f'executing: {command}')

        return OsCommandHandler.execute(command)
