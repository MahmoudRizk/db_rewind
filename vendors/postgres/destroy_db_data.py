import os

from vendors.postgres import switch_user

if __name__ == '__main__':
    user_name = os.environ['DB_REWINDER_HOST_POSTGRES_USER']
    switch_user(user_name=user_name)

    main_db_dir = os.environ["DB_REWINDER_POSTGRES_DATA_DIR"]

    command = f"rm -r {main_db_dir}/*"

    print("Destroying database files.")
    print(f"using command: {command}")

    os.system(command)
