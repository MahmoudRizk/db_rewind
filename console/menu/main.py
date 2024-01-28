from typing import List

from prompt_toolkit import PromptSession

from console.component.command import Command
from console.component.menu import Menu
from vendors.postgres.dbconnection import DBConnection
from vendors.postgres.setup import Setup as DBSetup
from vendors.postgres.db_rewinder import DBRewinder
from console.menu.setup import Setup as ConsoleSetup
from console.menu.rewinder import Rewinder as ConsoleRewinder


class Main(Menu):
    def __init__(self, session: PromptSession):
        super().__init__(session=session, prompt_name='')

    @staticmethod
    def setup(session: PromptSession, dbconnection: DBConnection, **kwargs):
        cursor = dbconnection.cursor()
        db_setup = DBSetup(cursor=cursor.cursor)
        ConsoleSetup(session=session).execute(
            session=session,
            db_setup=db_setup,
            dbconnection=dbconnection
        )

    @staticmethod
    def rewind(session: PromptSession, dbconnection: DBConnection, **kwargs):
        cursor = dbconnection.cursor()
        db_rewinder = DBRewinder(cursor=cursor.cursor)
        ConsoleRewinder(session=session).execute(
            session=session,
            db_rewinder=db_rewinder,
            dbconnection=dbconnection
        )

    def _get_commands(self) -> List[Command]:
        return [
            Command(
                name='help',
                description='Print available commands.',
                callback=lambda _: None
            ),
            Command(
                name='setup',
                description='Enter setup menu.',
                callback=Main.setup
            ),
            Command(
                name='rewinder',
                description='Enter DB rewinder menu.',
                callback=Main.rewind
            )
        ]
