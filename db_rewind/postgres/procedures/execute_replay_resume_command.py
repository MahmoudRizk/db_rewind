from typing import Optional
from db_rewind.postgres import from_env
from db_rewind.postgres.os_handler.os_command_handler import OsCommandHandler
from db_rewind.postgres.os_handler.os_response_dto import OsResponseDTO
from db_rewind.postgres.procedures.base_procedure import BaseProcedure


class ExecuteReplayResumeCommand(BaseProcedure):
    def execute_as_user(self) -> Optional[str]:
        return from_env('DB_REWINDER_HOST_POSTGRES_USER')

    def _execute(self) -> OsResponseDTO:
        command = 'psql -c "select pg_wal_replay_resume();"'
        self.print_info('resuming wal recovery, using pg_wal_replay_resume()')
        self.print_info(f'executing: {command}')

        return OsCommandHandler.execute(command)
