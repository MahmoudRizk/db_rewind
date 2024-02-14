import os

from vendors.postgres import switch_user


class CreateRecoverySignalFile:
    @staticmethod
    def execute():
        user_name = os.environ['DB_REWINDER_HOST_POSTGRES_USER']
        switch_user(user_name=user_name)

        main_db_dir = os.environ["DB_REWINDER_POSTGRES_DATA_DIR"]

        command = f"touch {main_db_dir}/recovery.signal"

        print('Creating recovery signal conf file')
        print(f"Using command: {command}")

        os.system(command)
