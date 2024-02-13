import os
import sys

from vendors.postgres import switch_user

if __name__ == '__main__':
    user_name = os.environ['DB_REWINDER_HOST_ROOT_USER']
    switch_user(user_name=user_name)

    command = sys.argv[1:][0]

    sys_command = f"systemctl {command} postgresql.service"
    print(f"{command} postgres server using systemctl: {sys_command}")

    os.system(sys_command)
