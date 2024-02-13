import os
import sys

from vendors.postgres import switch_user
from vendors.postgres.config_file_handler.file_handler import FileHandler

if __name__ == '__main__':
    user_name = os.environ['DB_REWINDER_HOST_POSTGRES_USER']
    switch_user(user_name=user_name)

    db_rewind_date = sys.argv[1:][0]

    print('Setting db rewind date in config file.')
    print(f"db_rewind_date: {db_rewind_date}")

    file_path = os.environ['DB_REWINDER_POSTGRES_CONFIG_FILE_PATH']

    config_file = FileHandler(file_path=file_path)

    config_file.set_directive_value('recovery_target_time', db_rewind_date, True)
    config_file.save()