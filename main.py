from vendors.postgres.dbconnection import DBConnection
from vendors.postgres.db_rewinder import DBRewinder
from vendors.postgres.setup import Setup

if __name__ == "__main__":
    database_name = "homestead"
    database_user = "postgres"
    database_password = "9Y2LEH8kMj"
    database_host = "127.0.0.1"
    database_port = "54320"

    connection = DBConnection(
        database_name=database_name,
        password=database_password,
        username=database_user,
        host=database_host,
        port=database_port
    )

    cursor = connection.cursor()

    db_setup = Setup(cursor=cursor.cursor)

    # db_setup.drop_trigger_function()
    # db_setup.drop_logs_table()

    # db_setup.create_logs_table()
    # db_setup.create_trigger_function()
    # db_setup.register_all_tables_to_trigger()

    db_rewinder: DBRewinder = DBRewinder(cursor=cursor.cursor)
    db_rewinder.rewind()


    connection.commit()

    cursor.cursor.close()
    connection.close()
