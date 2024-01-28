from typing import List

from prompt_toolkit import PromptSession

from console.component.command import Command
from console.component.menu import Menu
from vendors.postgres.dbconnection import DBConnection
from vendors.postgres.setup import Setup as DBSetup


class Setup(Menu):
    def __init__(self, session: PromptSession):
        super().__init__(session=session, prompt_name='setup')

    @staticmethod
    def install(db_setup: DBSetup, dbconnection: DBConnection, **kwargs) -> None:
        Setup.create_logs_table(db_setup=db_setup, dbconnection=dbconnection)
        Setup.create_watcher_function(db_setup=db_setup, dbconnection=dbconnection)
        Setup.register_all_tables_to_watcher_function(db_setup=db_setup, dbconnection=dbconnection)

    @staticmethod
    def uninstall(db_setup: DBSetup, dbconnection: DBConnection, **kwargs) -> None:
        Setup.unregister_all_tables_from_watcher_function(db_setup=db_setup, dbconnection=dbconnection)
        Setup.drop_watcher_function(db_setup=db_setup, dbconnection=dbconnection)
        Setup.drop_logs_table(db_setup=db_setup, dbconnection=dbconnection)

    @staticmethod
    def create_logs_table(db_setup: DBSetup, dbconnection: DBConnection, **kwargs) -> None:
        db_setup.create_logs_table()
        dbconnection.commit()

    @staticmethod
    def drop_logs_table(db_setup: DBSetup, dbconnection: DBConnection, **kwargs) -> None:
        db_setup.drop_logs_table()
        dbconnection.commit()

    @staticmethod
    def create_watcher_function(db_setup: DBSetup, dbconnection: DBConnection, **kwargs) -> None:
        db_setup.create_trigger_function()
        dbconnection.commit()

    @staticmethod
    def drop_watcher_function(db_setup: DBSetup, dbconnection: DBConnection, **kwargs) -> None:
        db_setup.drop_trigger_function()
        dbconnection.commit()

    @staticmethod
    def register_all_tables_to_watcher_function(db_setup: DBSetup, dbconnection: DBConnection, **kwargs) -> None:
        db_setup.register_all_tables_to_trigger()
        dbconnection.commit()

    @staticmethod
    def unregister_all_tables_from_watcher_function(db_setup: DBSetup, dbconnection: DBConnection, **kwargs) -> None:
        db_setup.unregister_all_tables_from_trigger()
        dbconnection.commit()

    @staticmethod
    def register_table_to_watcher_function(
            session: PromptSession,
            db_setup: DBSetup,
            dbconnection: DBConnection,
            **kwargs) -> None:
        table_name: str = session.prompt('Enter table name: ')
        db_setup.register_table_to_trigger(table_name=table_name)
        dbconnection.commit()

    @staticmethod
    def unregister_table_from_watcher_function(
            session: PromptSession,
            db_setup: DBSetup,
            dbconnection: DBConnection,
            **kwargs) -> None:
        table_name: str = session.prompt('Enter table name: ')
        db_setup.unregister_table_from_trigger(table_name=table_name)
        dbconnection.commit()

    def _get_commands(self) -> List[Command]:
        return [
            Command(
                name='help',
                description='print commands list',
                callback=lambda _: None
            ),
            Command(
                name='install',
                description='auto install database dependencies.',
                callback=Setup.install
            ),
            Command(
                name='uninstall',
                description='remove all dependencies added to the database.',
                callback=Setup.uninstall
            ),
            Command(
                name='create-logs-table',
                description='Create events logging table.',
                callback=Setup.create_logs_table
            ),
            Command(
                name='drop-logs-table',
                description='Drop events logging table.',
                callback=Setup.drop_logs_table
            ),
            Command(
                name='create-watcher-function',
                description='Create database watcher function.',
                callback=Setup.create_watcher_function
            ),
            Command(
                name='drop-watcher-function',
                description='Drop database watcher function.',
                callback=Setup.drop_watcher_function
            ),
            Command(
                name='register-all-tables-to-watcher-function',
                description='Register all tables to watcher function',
                callback=Setup.register_all_tables_to_watcher_function
            ),
            Command(
                name='unregister-all-tables-from-watcher-function',
                description='Unregister all tables from watcher function.',
                callback=Setup.unregister_all_tables_from_watcher_function
            ),
            Command(
                name='register-table-to-watcher-function',
                description='Register specific table to the watcher function',
                callback=Setup.register_table_to_watcher_function
            ),
            Command(
                name='unregister-table-from-watcher-function',
                description='Unregister specific table from the watcher function',
                callback=Setup.unregister_table_from_watcher_function
            )
        ]
