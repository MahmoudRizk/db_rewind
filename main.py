from vendors.postgres.dbconnection import DBConnection
from vendors.postgres.db_rewinder import DBRewinder

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

    db_rewinder: DBRewinder = DBRewinder(cursor=cursor.cursor)

    db_rewinder.rewind()

    # enable_trigger(cursor, "users")

    # create_t_history_table(cursor=cursor)
    # create_trigger_function(cursor=cursor)
    # register_tables(cursor=cursor)

    # print(res)

    # cursor.execute("select * from t_history;")
    # rows = cursor.fetchall()
    # print(rows)

    connection.commit()

    cursor.cursor.close()
    connection.close()
