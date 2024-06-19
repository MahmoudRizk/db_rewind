from typing import List

from prompt_toolkit import PromptSession

from db_rewind.console.component.command import Command
from db_rewind.console.component.menu import Menu
from db_rewind.postgres.db_rewinder import DBRewinder


class Rewinder(Menu):
    def __init__(self, session: PromptSession):
        super().__init__(session=session, prompt_name='DBRewinder')

    def rewind(self):
        DBRewinder.execute()

    def _get_commands(self) -> List[Command]:
        return [
            Command(
                name='rewind',
                description='Rewind Database',
                callback=self.rewind
            )
        ]
