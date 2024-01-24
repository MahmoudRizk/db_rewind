import json
from typing import List

from psycopg import Cursor, sql

from dbrewinder.abstract_db_rewinder import Log, AbstractDBRewinder, LogEvent


class DBRewinder(AbstractDBRewinder):
    def __init__(self, cursor: Cursor):
        self.cursor = cursor

    def disable_all_db_triggers(self):
        self.cursor.execute(
            """
                SET session_replication_role = replica;
            """
        )

    def enable_all_db_triggers(self):
        self.cursor.execute(
            """
                SET session_replication_role = DEFAULT;
            """
        )

    def get_logs(self) -> List[Log]:
        self.cursor.execute(
            """
                SELECT 
                    id,
                    tstamp,
                    tabname, 
                    operation, 
                    new_val, 
                    old_val
                FROM t_history
                ORDER BY id DESC;
            """
        )

        res = self.cursor.fetchall()

        return [
            Log(
                id=it[0],
                timestamp=it[1],
                table_name=it[2],
                operation=DBRewinder._map_to_operation_enum(it[3]),
                new_val=it[4],
                old_val=it[5]
            ) for it in res
        ]

    def update_from_json(self, table_name: str, json_value: dict):
        condition_column = "id"
        condition_value = json_value["id"]

        set_clause = sql.SQL(", ").join(
            [
                sql.Identifier(column) + sql.SQL(" = %s")
                for column in json_value.keys()
            ]
        )

        where_clause = sql.SQL("{} = %s").format(
            sql.Identifier(condition_column)
        )

        update_query = sql.SQL("UPDATE {} SET {} WHERE {}").format(
            sql.Identifier(table_name),
            set_clause,
            where_clause
        )

        update_data = []
        for key, value in json_value.items():
            if key in self._get_json_columns(table_name):
                value = json.dumps(value)
            update_data.append(value)

        update_data.append(condition_value)

        print(update_query.as_string(self.cursor))

        self.cursor.execute(update_query, update_data)

    def delete_from_json(self, table_name: str, json_value: dict):
        condition_column = 'id'
        condition_value = json_value['id']

        where_clause = sql.SQL("{} = %s").format(
            sql.Identifier(condition_column), condition_column
        )

        delete_query = sql.SQL("DELETE FROM {} where {}").format(
            sql.Identifier(table_name),
            where_clause
        )

        print(delete_query.as_string(self.cursor))

        self.cursor.execute(delete_query, [condition_value])

    def insert_from_json(self, table_name: str, json_value: dict):
        columns = sql.SQL(", ").join(
            [
                sql.Identifier(column)
                for column in json_value.keys()
            ]
        )

        values_place_holder = sql.SQL(", ").join(
            [
                sql.SQL("%s")
                for _ in range(0, len(json_value.keys()))
            ]
        )

        insert_statement = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            columns,
            values_place_holder
        )

        insert_data = []
        for key, value in json_value.items():
            if key in self._get_json_columns(table_name):
                value = json.dumps(value)
            insert_data.append(value)

        print(insert_statement.as_string(self.cursor))

        self.cursor.execute(insert_statement, insert_data)

    def flush_logs(self):
        self.cursor.execute(
            """
                DELETE FROM t_history;
            """
        )

    def _get_json_columns(self, table_name: str) -> list:
        self.cursor.execute(
            f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}' AND data_type in ('json', 'jsonb')
            """
        )

        return [it[0] for it in self.cursor.fetchall()]

    @staticmethod
    def _map_to_operation_enum(operation: str) -> LogEvent:
        match operation:
            case "INSERT":
                return LogEvent.INSERT
            case "UPDATE":
                return LogEvent.UPDATE
            case "DELETE":
                return LogEvent.DELETE
