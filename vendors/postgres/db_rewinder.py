import json
import time
from typing import List

from psycopg import sql, ClientCursor

from dbrewinder.abstract_db_rewinder import Log, AbstractDBRewinder, LogEvent


class DBRewinder(AbstractDBRewinder):
    def __init__(self, cursor: ClientCursor):
        self.cursor = cursor
        self.json_column_cache = {}

    def rewind(self):
        self.disable_all_db_triggers()

        tables_history_events: List[Log] = self.get_logs()

        sql_statements = []
        for row in tables_history_events:
            match row.operation:
                case LogEvent.UPDATE:
                    sql_statements.append(self.update_from_json(row.table_name, row.old_val))
                case LogEvent.INSERT:
                    sql_statements.append(self.delete_from_json(row.table_name, row.new_val))
                case LogEvent.DELETE:
                    sql_statements.append(self.insert_from_json(row.table_name, row.old_val))

        combined_sql_statements = ';'.join(sql_statements) + ';'
        self.cursor.execute(combined_sql_statements)

        self.flush_logs()
        self.enable_all_db_triggers()

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

    def update_from_json(self, table_name: str, json_value: dict) -> str:
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

        sql_statement = self.cursor.mogrify(update_query, update_data)
        print(sql_statement)
        return sql_statement

    def delete_from_json(self, table_name: str, json_value: dict) -> str:
        condition_column = 'id'
        condition_value = json_value['id']

        where_clause = sql.SQL("{} = %s").format(
            sql.Identifier(condition_column), condition_column
        )

        delete_query = sql.SQL("DELETE FROM {} where {}").format(
            sql.Identifier(table_name),
            where_clause
        )

        sql_statement = self.cursor.mogrify(delete_query, [condition_value])
        print(sql_statement)
        return sql_statement

    def insert_from_json(self, table_name: str, json_value: dict) -> str:
        start_time = time.time()
        columns = sql.SQL(", ").join(
            [
                sql.Identifier(column)
                for column in json_value.keys()
            ]
        )
        end_time = time.time()
        print(f"Execution time of column {end_time - start_time} seconds")

        start_time = time.time()
        values_place_holder = sql.SQL(", ").join(
            [
                sql.SQL("%s")
                for _ in range(0, len(json_value.keys()))
            ]
        )
        end_time = time.time()
        print(f"Execution values_place_holder of column {end_time - start_time} seconds")

        start_time = time.time()
        insert_statement = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            columns,
            values_place_holder
        )
        end_time = time.time()
        print(f"Execution insert_statement of column {end_time - start_time} seconds")

        start_time = time.time()
        insert_data = []
        for key, value in json_value.items():
            if key in self._get_json_columns(table_name):
                value = json.dumps(value)
            insert_data.append(value)
        end_time = time.time()
        print(f"Execution data_parsing of column {end_time - start_time} seconds")

        start_time = time.time()
        sql_statement = self.cursor.mogrify(insert_statement, insert_data)
        end_time = time.time()
        print(f"Execution cursor.mogrify of column {end_time - start_time} seconds")

        print(sql_statement)
        return sql_statement


    def flush_logs(self):
        self.cursor.execute(
            """
                DELETE FROM t_history;
            """
        )

    def _get_json_columns(self, table_name: str) -> list:
        if table_name in self.json_column_cache:
            print(f"table name {table_name} found in cache.")
            return self.json_column_cache.get(table_name)

        print(f"table name {table_name} cache missing.")
        self.cursor.execute(
            f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}' AND data_type in ('json', 'jsonb')
            """
        )

        res = [it[0] for it in self.cursor.fetchall()]
        self.json_column_cache[table_name] = res

        return res

    @staticmethod
    def _map_to_operation_enum(operation: str) -> LogEvent:
        match operation:
            case "INSERT":
                return LogEvent.INSERT
            case "UPDATE":
                return LogEvent.UPDATE
            case "DELETE":
                return LogEvent.DELETE
