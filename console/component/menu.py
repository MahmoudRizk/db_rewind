import abc
from abc import abstractmethod
from typing import List, Optional

from prompt_toolkit import PromptSession

from console.component.command import Command


class Menu(metaclass=abc.ABCMeta):
    def __init__(self, session: PromptSession, prompt_name: str = ""):
        self.commands = self.get_commands()
        self.session: PromptSession = session
        self.prompt_name: str = prompt_name

    def execute(self, **kwargs):
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
                command.get_callback()(**kwargs)

    @staticmethod
    def get_command(command_name: str, commands: List[Command]) -> Optional[Command]:
        matched_commands: List[Command] = list(filter(lambda command: command.get_name() == command_name, commands))
        return matched_commands and matched_commands[0] or None

    @staticmethod
    def convert_from_kebab_to_snake_case(txt: str) -> str:
        return txt.replace('-', '_')

    def print_commands_for_help(self) -> None:
        print('command', 'description')
        for command in self.commands:
            print(command.get_name(), command.get_description())

    def get_commands(self) -> List[Command]:
        commands = self._get_commands()

        # Add exit commands if was not defined in the list of commands.
        if not Menu.get_command('exit', commands):
            commands.append(
                Command(
                    'exit',
                    'exit menu',
                    callback=lambda **kwargs: None
                )
            )
        return commands

    @abstractmethod
    def _get_commands(self) -> List[Command]:
        pass
