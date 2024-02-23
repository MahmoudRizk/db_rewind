from typing import List

from prompt_toolkit import PromptSession

from console.component.command import Command
from console.component.menu import Menu
from vendors.postgres.db_rewinder import DBRewinder


class Rewinder(Menu):
    def __init__(self, session: PromptSession):
        super().__init__(session=session, prompt_name='DBRewinder')

    def rewind(self):
        DBRewinder.execute()

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
                callback=self.rewind
            )
        ]
