from vendors.postgres.config_file_setup import ConfigFileSetup

config_file_path = '/home/mahmoudrizk/db_time_travel/vendors/postgres/postgresql.conf'
db_data_directory = ''

if __name__ == '__main__':
    config_file_setup = ConfigFileSetup(file_path=config_file_path)
    config_file_setup.execute()
