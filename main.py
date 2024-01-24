import psycopg
from psycopg import Cursor, sql
from typing import Optional
from psycopg.errors import DuplicateTable, DuplicateFunction, UndefinedObject
import json

from vendors.postgres.dbconnection import DBConnection
from vendors.postgres.db_rewinder import DBRewinder

# class CursorResponse:
#     def __init__(self, success: bool, message: Optional[str]):
#         self.success = success
#         self.message = message
#
#     @staticmethod
#     def success() -> "CursorResponse":
#         return CursorResponse(success=True, message=None)
#
#     @staticmethod
#     def failed(message: str) -> "CursorResponse":
#         return CursorResponse(success=False, message=message)
#
#
# def construct_database_uri(
#         database_name: str,
#         username: str = "postgres",
#         password: str = "postgres",
#         host: str = "127.0.0.1",
#         port: str = "5432",
# ) -> str:
#     return f"postgresql://{username}:{password}@{host}:{port}/{database_name}"
#
#
# def create_t_history_table(cursor: Cursor) -> CursorResponse:
#     try:
#         cursor.execute(
#             """
#                 CREATE TABLE IF NOT EXISTS t_history(
#                     id serial,
#                     tstamp timestamp default now(),
#                     tabname text,
#                     operation text,
#                     new_val json,
#                     old_val json
#                 );
#             """
#         )
#     except DuplicateTable as e:
#         return CursorResponse.failed(message=str(e))
#     else:
#         return CursorResponse.success()
#
#
# def create_trigger_function(cursor: Cursor) -> CursorResponse:
#     try:
#         cursor.execute(
#             """
#                 CREATE OR REPLACE FUNCTION change_trigger()
#                     RETURNS trigger
#                     LANGUAGE PLPGSQL
#                 AS $$
#                 BEGIN
#                     IF      TG_OP = 'INSERT'
#                     THEN
#                         INSERT INTO t_history (tabname, operation, new_val)
#                             VALUES (TG_RELNAME, TG_OP, row_to_json(NEW));
#                             RETURN NEW;
#                     ELSIF   TG_OP = 'UPDATE'
#                     THEN
#                         INSERT INTO t_history (tabname, operation, new_val, old_val)
#                             VALUES (TG_RELNAME, TG_OP, row_to_json(NEW), row_to_json(OLD));
#                         RETURN NEW;
#                     ELSIF   TG_OP = 'DELETE'
#                     THEN
#                         INSERT INTO t_history (tabname, operation, old_val)
#                             VALUES (TG_RELNAME, TG_OP, row_to_json(OLD));
#                         RETURN OLD;
#                     END IF;
#                 END;
#                 $$
#             """
#         )
#     except DuplicateFunction as e:
#         return CursorResponse.failed(str(e))
#     else:
#         return CursorResponse.success()
#
#
# def register_table_to_trigger(cursor: Cursor, table_name: str):
#     cursor.execute(
#         f"""
#             CREATE OR REPLACE TRIGGER trigger_{table_name}
#             BEFORE INSERT OR UPDATE OR DELETE ON {table_name}
#             FOR EACH ROW EXECUTE PROCEDURE change_trigger();
#         """
#     )
#
#
# def disable_trigger(cursor: Cursor, table_name: str):
#     try:
#         cursor.execute(
#             f"""
#                 ALTER TABLE {table_name}
#                 DISABLE TRIGGER trigger_{table_name};
#             """
#         )
#     except UndefinedObject as e:
#         return CursorResponse.failed(str(e))
#     else:
#         return CursorResponse.success()
#
#
# def enable_trigger(cursor: Cursor, table_name: str) -> CursorResponse:
#     try:
#         cursor.execute(
#             f"""
#                 ALTER TABLE {table_name}
#                 ENABLE TRIGGER trigger_{table_name};
#             """
#         )
#     except UndefinedObject as e:
#         return CursorResponse.failed(str(e))
#     else:
#         return CursorResponse.success()
#
#
# def register_tables(cursor: Cursor):
#     tables = cursor.execute(
#         """
#             SELECT
#                 table_name
#             FROM information_schema.tables
#             WHERE
#                 table_schema = 'public'
#                 AND
#                     table_type = 'BASE TABLE'
#                 AND
#                     table_name != 't_history' ;
#         """
#     )
#     for tab in tables.fetchall():
#         register_table_to_trigger(cursor=cursor, table_name=tab[0])
#
#
# def flush_t_history_table(cursor: Cursor):
#     cursor.execute(
#         """
#             DELETE FROM t_history;
#         """
#     )
#
#
# def disable_all_db_triggers(cursor: Cursor):
#     cursor.execute(
#         """
#             SET session_replication_role = replica;
#         """
#     )
#
#
# def enable_all_db_triggers(cursor: Cursor):
#     cursor.execute(
#         """
#             SET session_replication_role = DEFAULT;
#         """
#     )
#
#
# def get_json_columns(table_name: str) -> list:
#     cursor.execute(
#         f"""
#             SELECT column_name
#             FROM information_schema.columns
#             WHERE table_name = '{table_name}' AND data_type in ('json', 'jsonb')
#         """
#     )
#
#     return [it[0] for it in cursor.fetchall()]
#
#
# def db_rewind(cursor: Cursor):
#     disable_all_db_triggers(cursor)
#
#     history_events = cursor.execute(
#         """
#             SELECT
#                 tabname,
#                 operation,
#                 new_val,
#                 old_val
#             FROM t_history
#             ORDER BY id DESC;
#         """
#     )
#
#     history_events = cursor.fetchall()
#
#     for it in history_events:
#         table_name = it[0]
#         operation = it[1]
#         new_val = it[2]
#         old_val = it[3]
#
#         json_columns: list = get_json_columns(table_name)
#
#         match operation:
#             case "UPDATE":
#                 update_from_json(cursor, table_name, old_val, json_columns)
#             case "INSERT":
#                 delete_from_json(cursor, table_name, new_val)
#             case "DELETE":
#                 insert_from_json(cursor, table_name, old_val, json_columns)
#
#     flush_t_history_table(cursor)
#     enable_all_db_triggers(cursor)
#
#
# def update_from_json(cursor: Cursor, table_name: str, json_value: dict, json_columns: list):
#     condition_column = "id"
#     condition_value = json_value["id"]
#
#     set_clause = sql.SQL(", ").join(
#         [
#             sql.Identifier(column) + sql.SQL(" = %s")
#             for column in json_value.keys()
#         ]
#     )
#
#     where_clause = sql.SQL("{} = %s").format(
#         sql.Identifier(condition_column)
#     )
#
#     update_query = sql.SQL("UPDATE {} SET {} WHERE {}").format(
#         sql.Identifier(table_name),
#         set_clause,
#         where_clause
#     )
#
#     update_data = []
#     for key, value in json_value.items():
#         if key in json_columns:
#             value = json.dumps(value)
#         update_data.append(value)
#
#     update_data.append(condition_value)
#
#     print(update_query.as_string(cursor))
#
#     cursor.execute(update_query, update_data)
#
#
# def delete_from_json(cursor: Cursor, table_name: str, json_value: dict):
#     condition_column = 'id'
#     condition_value = json_value['id']
#
#     where_clause = sql.SQL("{} = %s").format(
#         sql.Identifier(condition_column), condition_column
#     )
#
#     delete_query = sql.SQL("DELETE FROM {} where {}").format(
#         sql.Identifier(table_name),
#         where_clause
#     )
#
#     print(delete_query.as_string(cursor))
#
#     cursor.execute(delete_query, [condition_value])
#
#
# def insert_from_json(cursor: Cursor, table_name: str, json_value: dict, json_columns: list):
#     columns = sql.SQL(", ").join(
#         [
#             sql.Identifier(column)
#             for column in json_value.keys()
#         ]
#     )
#
#     values_place_holder = sql.SQL(", ").join(
#         [
#             sql.SQL("%s")
#             for _ in range(0, len(json_value.keys()))
#         ]
#     )
#
#     insert_statement = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
#         sql.Identifier(table_name),
#         columns,
#         values_place_holder
#     )
#
#     insert_data = []
#     for key, value in json_value.items():
#         if key in json_columns:
#             value = json.dumps(value)
#         insert_data.append(value)
#
#     print(insert_statement.as_string(cursor))
#
#     cursor.execute(insert_statement, insert_data)


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

    cursor.close()
    connection.close()
