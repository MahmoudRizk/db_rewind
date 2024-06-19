from typing import Optional

from db_rewind.postgres import from_env
from db_rewind.postgres.config_file_handler.file_handler import FileHandler
from db_rewind.postgres.config_file_handler.file_io import FileIO
from db_rewind.postgres.os_handler.os_response_dto import OsResponseDTO
from db_rewind.postgres.procedures.base_procedure import BaseProcedure


class SetDBRewindDate(BaseProcedure):
    def execute_as_user(self) -> Optional[str]:
        return from_env('DB_REWINDER_HOST_POSTGRES_USER')

    def _execute(self):
        self.print_message('Please enter date time to rewind to in format YYYY-mm-dd HH:MM:SS :')

        db_rewind_date = self.prompt_session.prompt('enter date:')

        self.print_info('Setting db rewind date in config file.')
        self.print_info(f"db_rewind_date: {db_rewind_date}")

        file_path = from_env('DB_REWINDER_POSTGRES_CONFIG_FILE_PATH')
        file_io = FileIO(file_path)
        config_file = FileHandler(file_io=file_io)

        config_file.set_directive_value('recovery_target_time', db_rewind_date, True)
        config_file.save()

        return OsResponseDTO(exit_code=0)
