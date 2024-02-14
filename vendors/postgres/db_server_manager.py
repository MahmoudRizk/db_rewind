import os

from vendors.postgres import switch_user


class DBServerManager:
    @staticmethod
    def execute(command: str):
        user_name = os.environ['DB_REWINDER_HOST_ROOT_USER']
        switch_user(user_name=user_name)

        sys_command = f"systemctl {command} postgresql.service"
        print(f"{command} postgres server using systemctl: {sys_command}")

        os.system(sys_command)
