from vendors.postgres.dbconnection import DBConnection
from vendors.postgres.db_rewinder import DBRewinder
from vendors.postgres.setup import Setup as DBSetup
from console.menu.setup import Setup as ConsoleSetup

import click
from prompt_toolkit import prompt, PromptSession


def main_menu(session: PromptSession, dbconnection: DBConnection):
    commands = [
        'help',
        'exit',
        'setup',
        'rewinder',
    ]

    while True:
        command = session.prompt('>: ')

        match command:
            case 'exit':
                break
            case 'setup':
                cursor = dbconnection.cursor()
                db_setup = DBSetup(cursor=cursor.cursor)
                ConsoleSetup(session=session).execute(
                    session=session,
                    db_setup=db_setup,
                    dbconnection=dbconnection
                )
            case 'rewinder':
                cursor = dbconnection.cursor()
                db_rewinder = DBRewinder(cursor=cursor.cursor)
                db_rewinder_menu(session=session, db_rewinder=db_rewinder, dbconnection=dbconnection)
            case _:
                print('available commands')
                print(commands)


def db_rewinder_menu(session: PromptSession, db_rewinder: DBRewinder, dbconnection: DBConnection):
    commands = [
        'help',
        'exit',
        'rewind'
    ]

    def rewind():
        db_rewinder.rewind()
        dbconnection.commit()

    while True:
        command = session.prompt('>DBRewinder: ')

        match command:
            case 'exit':
                break
            case 'rewind':
                rewind()
            case _:
                print('available commands')
                print(commands)


def setup_menu(session: PromptSession, db_setup: DBSetup, dbconnection: DBConnection):
    commands = [
        'help',
        'exit',
        'install',
        'uninstall',
        'create-logs-table',
        'drop-logs-table',
        'create-watcher-function',
        'drop-watcher-function',
        'register-all-tables-to-watcher-function',
        'unregister-all-tables-from-watcher-function',
        'register-table-to-watcher-function',
        'unregister-table-from-watcher-function',
    ]

    def install():
        create_logs_table()
        create_watcher_function()
        register_all_tables_to_watcher_function()

    def uninstall():
        unregister_all_tables_from_watcher_function()
        drop_watcher_function()
        drop_logs_table()

    def create_logs_table():
        db_setup.create_logs_table()
        dbconnection.commit()

    def drop_logs_table():
        db_setup.drop_logs_table()
        dbconnection.commit()

    def create_watcher_function():
        db_setup.create_trigger_function()
        dbconnection.commit()

    def drop_watcher_function():
        db_setup.drop_trigger_function()
        dbconnection.commit()

    def register_all_tables_to_watcher_function():
        db_setup.register_all_tables_to_trigger()
        dbconnection.commit()

    def unregister_all_tables_from_watcher_function():
        db_setup.unregister_all_tables_from_trigger()
        dbconnection.commit()

    def register_table_to_watcher_function():
        table_name: str = session.prompt('Enter table name: ')
        db_setup.register_table_to_trigger(table_name=table_name)
        dbconnection.commit()

    def unregister_table_from_watcher_function():
        table_name: str = session.prompt('Enter table name: ')
        db_setup.unregister_table_from_trigger(table_name=table_name)
        dbconnection.commit()

    while True:
        command = session.prompt('>setup: ')

        match command:
            case 'exit':
                break
            case 'install':
                install()
            case 'uninstall':
                uninstall()
            case 'create-logs-table':
                create_logs_table()
            case 'drop-logs-table':
                drop_logs_table()
            case 'create-watcher-function':
                create_watcher_function()
            case 'drop-watcher-function':
                drop_watcher_function()
            case 'register-all-tables-to-watcher-function':
                register_all_tables_to_watcher_function()
            case 'unregister-all-tables-from-watcher-function':
                unregister_all_tables_from_watcher_function()
            case 'register-table-to-watcher-function':
                register_table_to_watcher_function()
            case 'unregister-table-from-watcher-function':
                unregister_table_from_watcher_function()
            case _:
                print('available commands')
                print(commands)


@click.command()
@click.option('--db_name', required=True, help='Database name.')
@click.option('--db_user', required=True, help='Database user.')
@click.option('--db_password', required=True, help='Database password.')
@click.option('--db_host', default='localhost', help='Database host.')
@click.option('--db_port', default='5432', help='Database port.')
def main(db_name: str, db_user: str, db_password: str, db_host: str, db_port: str):
    session = PromptSession()
    dbconnection = DBConnection(
        database_name=db_name,
        password=db_password,
        username=db_user,
        host=db_host,
        port=db_port
    )

    main_menu(session, dbconnection)

    # while True:
    #     try:
    #         text = session.prompt('> ')
    #     except KeyboardInterrupt:
    #         continue
    #     except EOFError:
    #         break
    #     else:
    #         if text == 'install':
    #             dbconnection = DBConnection(
    #                 database_name=db_name,
    #                 password=db_password,
    #                 username=db_user,
    #                 host=db_host,
    #                 port=db_port
    #             )
    #
    #             cursor = dbconnection.cursor()
    #
    #             db_setup = Setup(cursor=cursor.cursor)
    #
    #             db_setup.create_logs_table()
    #             db_setup.create_trigger_function()
    #             db_setup.register_all_tables_to_trigger()
    #
    #             dbconnection.commit()
    #
    #             cursor.cursor.close()
    #             dbconnection.close()
    #         elif text == 'uninstall':
    #             dbconnection = DBConnection(
    #                 database_name=db_name,
    #                 password=db_password,
    #                 username=db_user,
    #                 host=db_host,
    #                 port=db_port
    #             )
    #
    #             cursor = dbconnection.cursor()
    #
    #             db_setup = Setup(cursor=cursor.cursor)
    #
    #             db_setup.drop_trigger_function()
    #             db_setup.drop_logs_table()
    #
    #             dbconnection.commit()
    #
    #             cursor.cursor.close()
    #             dbconnection.close()
    #         elif text == 'db-rewind':
    #             dbconnection = DBConnection(
    #                 database_name=db_name,
    #                 password=db_password,
    #                 username=db_user,
    #                 host=db_host,
    #                 port=db_port
    #             )
    #
    #             cursor = dbconnection.cursor()
    #
    #             db_rewinder: DBRewinder = DBRewinder(cursor=cursor.cursor)
    #             db_rewinder.rewind()
    #
    #             dbconnection.commit()
    #
    #             cursor.cursor.close()
    #             dbconnection.close()
    #         else:
    #             print("Unknown command")
    #             print("available commands [install, uninstall & db-rewind]")

    print('GoodBye!')


if __name__ == "__main__":
    main()
