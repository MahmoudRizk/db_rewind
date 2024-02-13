import os

from vendors.postgres import switch_user

if __name__ == '__main__':
    user_name = os.environ['DB_REWINDER_HOST_POSTGRES_USER']
    switch_user(user_name=user_name)

    base_backup_dir = os.environ["DB_REWINDER_POSTGRES_BASE_BACKUP_DIR"]
    main_db_dir = os.environ["DB_REWINDER_POSTGRES_DATA_DIR"]

    backup_file_name = 'db_rewinder.tar.gz'

    # Set database in backup mode first using.
    command = "psql -c \"SELECT pg_start_backup('label');\""
    print('Running pg_start_backup.')
    print(f"using command: {command}")
    os.system(command)

    # Backing up database.
    command = f"tar -czf {base_backup_dir}/{backup_file_name} -C {main_db_dir} --exclude=pg_wal ."
    print('creating db backup.')
    print(f"using: {command}")
    os.system(command)

    # Stop database backup mode.
    command = 'psql -c "SELECT pg_stop_backup();"'
    print('Running pg_stop_backup.')
    print(f"using command: {command}")
    os.system(command)
