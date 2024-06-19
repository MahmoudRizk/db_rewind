import abc
from abc import abstractmethod
from typing import List, Optional

from prompt_toolkit import PromptSession

from db_rewind.console.component.command import Command


class Menu(metaclass=abc.ABCMeta):
    def __init__(self, session: PromptSession, prompt_name: str = ""):
        self.commands = self.get_commands()
        self.session: PromptSession = session
        self.prompt_name: str = prompt_name

    def execute(self):
        while True:
            cli_input = Menu.convert_from_kebab_to_snake_case(
                self.session.prompt(f">{self.prompt_name}: ")
            )

            if cli_input == 'exit':
                break

            command = Menu.get_command(command_name=cli_input, commands=self.commands)

            if not command:
                self.print_commands_for_help()
            else:
                command.get_callback()()

    @staticmethod
    def get_command(command_name: str, commands: List[Command]) -> Optional[Command]:
        matched_commands: List[Command] = list(filter(lambda command: command.get_name() == command_name, commands))
        return matched_commands and matched_commands[0] or None

    @staticmethod
    def convert_from_kebab_to_snake_case(txt: str) -> str:
        return txt.replace('-', '_')

    def print_commands_for_help(self) -> None:
        print('\nAvailable Commands\n')
        for command in self.commands:
            print(f'\t{command.get_name()} - {command.get_description()}')

        print('\n')

    def get_commands(self) -> List[Command]:
        commands = self._get_commands()

        commands.append(
            Command(
                'exit',
                'exit menu',
                callback=lambda **kwargs: None
            )
        )
        commands.append(
            Command(
                name='help',
                description='list available commands',
                callback=lambda **kwargs: self.print_commands_for_help()
            )
        )

        return commands

    @abstractmethod
    def _get_commands(self) -> List[Command]:
        pass
