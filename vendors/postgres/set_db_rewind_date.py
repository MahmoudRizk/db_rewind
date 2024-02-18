from vendors.postgres import from_env
from vendors.postgres.config_file_handler.file_handler import FileHandler
from vendors.postgres.os_handler.os_new_process_handler import OsNewProcessHandler


class SetDBRewindDate:
    @staticmethod
    @OsNewProcessHandler.in_new_process(as_user=from_env('DB_REWINDER_HOST_POSTGRES_USER'))
    def execute(db_rewind_date: str):
        print('Setting db rewind date in config file.')
        print(f"db_rewind_date: {db_rewind_date}")

        file_path = from_env('DB_REWINDER_POSTGRES_CONFIG_FILE_PATH')

        config_file = FileHandler(file_path=file_path)

        config_file.set_directive_value('recovery_target_time', db_rewind_date, True)
        config_file.save()
