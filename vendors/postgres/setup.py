from psycopg import Cursor

from dbrewinder.abstract_setup import AbstractSetup


class Setup(AbstractSetup):
    def __init__(self, cursor: Cursor):
        self.cursor = cursor

    def create_logs_table(self):
        print("Create t_history table if not exists.")
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS t_history(
                    id serial,
                    tstamp timestamp default now(),
                    tabname text,
                    operation text,
                    new_val json,
                    old_val json
                );
            """
        )

    def drop_logs_table(self):
        print("Dropping t_history table")
        self.cursor.execute(
            """
                DROP TABLE IF EXISTS t_history CASCADE;
            """
        )

    def create_trigger_function(self):
        print("Create or replace change_trigger function.")
        self.cursor.execute(
            """
                CREATE OR REPLACE FUNCTION change_trigger() 
                    RETURNS trigger 
                    LANGUAGE PLPGSQL
                AS $$
                BEGIN
                    IF      TG_OP = 'INSERT'
                    THEN
                        INSERT INTO t_history (tabname, operation, new_val)
                            VALUES (TG_RELNAME, TG_OP, row_to_json(NEW));
                            RETURN NEW;
                    ELSIF   TG_OP = 'UPDATE'
                    THEN
                        INSERT INTO t_history (tabname, operation, new_val, old_val)
                            VALUES (TG_RELNAME, TG_OP, row_to_json(NEW), row_to_json(OLD));
                        RETURN NEW;
                    ELSIF   TG_OP = 'DELETE'
                    THEN
                        INSERT INTO t_history (tabname, operation, old_val)
                            VALUES (TG_RELNAME, TG_OP, row_to_json(OLD));
                        RETURN OLD;
                    END IF;
                END;
                $$
            """
        )

    def drop_trigger_function(self):
        print("Drop change_trigger function.")
        self.cursor.execute("""
            DROP FUNCTION IF EXISTS change_trigger() CASCADE;
        """)

    def register_table_to_trigger(self, table_name: str):
        self.unregister_table_from_trigger(table_name=table_name)
        print(f"Registering {table_name} to change_trigger function.")
        self.cursor.execute(
            f"""
                    CREATE TRIGGER trigger_{table_name}
                    BEFORE INSERT OR UPDATE OR DELETE ON {table_name}
                    FOR EACH ROW EXECUTE PROCEDURE change_trigger();
                """
        )

    def unregister_table_from_trigger(self, table_name: str):
        print(f"unregistering {table_name} from change_trigger function.")
        self.cursor.execute(
            f"""
                DROP TRIGGER IF EXISTS trigger_{table_name} ON {table_name}
            """
        )

    def register_all_tables_to_trigger(self):
        print("Registering all tables to change_trigger function.")
        for tab in self._get_tables():
            self.register_table_to_trigger(table_name=tab[0])

    def unregister_all_tables_from_trigger(self):
        print("Unregistering all tables from change_trigger function.")
        for tab in self._get_tables():
            self.unregister_table_from_trigger(table_name=tab[0])

    def _get_tables(self):
        res = self.cursor.execute(
            """
                SELECT 
                    table_name 
                FROM information_schema.tables 
                WHERE 
                    table_schema = 'public' 
                    AND 
                        table_type = 'BASE TABLE'
                    AND 
                        table_name != 't_history' ;
            """
        )

        return res.fetchall()
