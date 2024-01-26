from vendors.postgres.dbconnection import DBConnection
from vendors.postgres.db_rewinder import DBRewinder
from vendors.postgres.setup import Setup
import click
from prompt_toolkit import prompt, PromptSession


@click.command()
@click.option('--db_name', required=True, help='Database name.')
@click.option('--db_user', required=True, help='Database user.')
@click.option('--db_password', required=True, help='Database password.')
@click.option('--db_host', default='localhost', help='Database host.')
@click.option('--db_port', default='5432', help='Database port.')
def main(db_name: str, db_user: str, db_password: str, db_host: str, db_port: str):
    session = PromptSession()
    while True:
        try:
            text = session.prompt('> ')
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            if text == 'install':
                dbconnection = DBConnection(
                    database_name=db_name,
                    password=db_password,
                    username=db_user,
                    host=db_host,
                    port=db_port
                )

                cursor = dbconnection.cursor()

                db_setup = Setup(cursor=cursor.cursor)

                db_setup.create_logs_table()
                db_setup.create_trigger_function()
                db_setup.register_all_tables_to_trigger()

                dbconnection.commit()

                cursor.cursor.close()
                dbconnection.close()
            elif text == 'uninstall':
                dbconnection = DBConnection(
                    database_name=db_name,
                    password=db_password,
                    username=db_user,
                    host=db_host,
                    port=db_port
                )

                cursor = dbconnection.cursor()

                db_setup = Setup(cursor=cursor.cursor)

                db_setup.drop_trigger_function()
                db_setup.drop_logs_table()

                dbconnection.commit()

                cursor.cursor.close()
                dbconnection.close()
            elif text == 'db-rewind':
                dbconnection = DBConnection(
                    database_name=db_name,
                    password=db_password,
                    username=db_user,
                    host=db_host,
                    port=db_port
                )

                cursor = dbconnection.cursor()

                db_rewinder: DBRewinder = DBRewinder(cursor=cursor.cursor)
                db_rewinder.rewind()

                dbconnection.commit()

                cursor.cursor.close()
                dbconnection.close()
            else:
                print("Unknown command")
                print("available commands [install, uninstall & db-rewind]")

    print('GoodBye!')


if __name__ == "__main__":
    main()
