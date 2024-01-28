from typing import List

from prompt_toolkit import PromptSession

from console.component.command import Command
from console.component.menu import Menu
from vendors.postgres.db_rewinder import DBRewinder
from vendors.postgres.dbconnection import DBConnection


class Rewinder(Menu):
    def __init__(self, session: PromptSession):
        super().__init__(session=session, prompt_name='DBRewinder')

    @staticmethod
    def rewind(db_rewinder: DBRewinder, dbconnection: DBConnection, **kwargs):
        db_rewinder.rewind()
        dbconnection.commit()

    def _get_commands(self) -> List[Command]:
        return [
            Command(
                name='help',
                description='print available commands',
                callback=lambda _: None
            ),
            Command(
                name='rewind',
                description='Rewind Database',
                callback=Rewinder.rewind
            )
        ]
