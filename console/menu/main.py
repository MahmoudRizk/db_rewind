from typing import List

from prompt_toolkit import PromptSession

from console.component.command import Command
from console.component.menu import Menu
from console.menu.setup import Setup as ConsoleSetup


class Main(Menu):
    def __init__(self, session: PromptSession):
        super().__init__(session=session, prompt_name='')

    @staticmethod
    def setup(session: PromptSession, **kwargs):
        ConsoleSetup(session=session).execute(
            session=session,
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
        ]
