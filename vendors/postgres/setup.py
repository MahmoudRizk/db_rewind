from psycopg import Cursor

from dbrewinder.abstract_setup import AbstractSetup


class Setup(AbstractSetup):
    def __init__(self, cursor: Cursor):
        self.cursor = cursor

    def create_logs_table(self):
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

    def create_trigger_function(self):
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

    def register_table_to_trigger(self, table_name: str):
        self.cursor.execute(
            f"""
                    CREATE OR REPLACE TRIGGER trigger_{table_name}
                    BEFORE INSERT OR UPDATE OR DELETE ON {table_name}
                    FOR EACH ROW EXECUTE PROCEDURE change_trigger();
                """
        )

    def register_all_tables_to_trigger(self):
        tables = self.cursor.execute(
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
        for tab in tables.fetchall():
            self.register_table_to_trigger(table_name=tab[0])
