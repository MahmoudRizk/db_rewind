import os

from vendors.postgres import switch_user


class RestoreDBBaseBackup:
    @staticmethod
    def execute():
        user_name = os.environ['DB_REWINDER_HOST_POSTGRES_USER']
        switch_user(user_name=user_name)

        base_backup_dir = os.environ["DB_REWINDER_POSTGRES_BASE_BACKUP_DIR"]
        main_db_dir = os.environ["DB_REWINDER_POSTGRES_DATA_DIR"]

        "tar xvfz /var/lib/postgresql/base_backup_12/base.tar -C ./"

        # TODO: solve hard coded file name.
        backup_file_name = 'db_rewinder.tar.gz'

        command = f"tar xfz {base_backup_dir}/{backup_file_name} -C {main_db_dir}"

        print("Restoring db base backup.")
        print(f"using command: {command}")

        os.system(command)

        command = f"mkdir {main_db_dir}/pg_wal"
        print("Creating missing pg_wal directory")
        print(f"using command: {command}")

        os.system(command)
