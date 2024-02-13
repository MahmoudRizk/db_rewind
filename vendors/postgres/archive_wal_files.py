import os

from vendors.postgres import switch_user

if __name__ == '__main__':
    user_name = os.environ['DB_REWINDER_HOST_POSTGRES_USER']
    switch_user(user_name=user_name)

    print('archiving wal files, using pg_switch_wal()')
    print('executing: psql -c "select pg_switch_wal();"')
    os.system('psql -c "select pg_switch_wal();"')