from typing import List

from prompt_toolkit import PromptSession

from console.component.command import Command
from console.component.menu import Menu
from console.menu.setup import Setup as ConsoleSetup
from console.menu.rewinder import Rewinder as DBRewinder


class Main(Menu):
    def __init__(self, session: PromptSession):
        super().__init__(session=session, prompt_name='')

    def setup(self):
        ConsoleSetup(session=self.session).execute()

    def rewinder(self):
        DBRewinder(session=self.session).execute()

    def _get_commands(self) -> List[Command]:
        return [
            Command(
                name='setup',
                description='Enter setup menu.',
                callback=self.setup
            ),
            Command(
                name='rewinder',
                description='Rewinder menu',
                callback=self.rewinder
            ),
        ]
