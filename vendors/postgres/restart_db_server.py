import os

from vendors.postgres import switch_user

if __name__ == '__main__':
    user_name = os.environ['DB_REWINDER_HOST_ROOT_USER']
    switch_user(user_name=user_name)

    command = 'systemctl restart postgresql.service'
    print(f"Restart postgres server using systemctl: {command}")

    os.system(command)
