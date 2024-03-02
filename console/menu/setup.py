from typing import List

from prompt_toolkit import PromptSession

from console.component.command import Command
from console.component.menu import Menu
from vendors.postgres.db_setup import DBSetup


class Setup(Menu):
    def __init__(self, session: PromptSession):
        super().__init__(session=session, prompt_name='setup')

    @staticmethod
    def install() -> None:
        DBSetup().execute()

    def _get_commands(self) -> List[Command]:
        return [
            Command(
                name='install',
                description='auto install database dependencies.',
                callback=Setup.install
            ),
        ]
