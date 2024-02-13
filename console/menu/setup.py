import subprocess
import sys

from typing import List

from prompt_toolkit import PromptSession

from console.component.command import Command
from console.component.menu import Menu


class Setup(Menu):
    def __init__(self, session: PromptSession):
        super().__init__(session=session, prompt_name='setup')

    @staticmethod
    def install(**kwargs) -> None:
        Setup.configure_postgres_conf_file()
        Setup.restart_postgres_server()

        Setup.archive_wal_files()
        Setup.create_db_base_backup()

    @staticmethod
    def configure_postgres_conf_file(**kwargs):
        subprocess.run([sys.executable, '-m', 'vendors.postgres.config_file_setup'])

    @staticmethod
    def restart_postgres_server(**kwargs):
        subprocess.run([sys.executable, '-m', 'vendors.postgres.db_server_manager', 'restart'])

    @staticmethod
    def archive_wal_files():
        subprocess.run([sys.executable, '-m', 'vendors.postgres.archive_wal_files'])

    @staticmethod
    def create_db_base_backup():
        subprocess.run([sys.executable, '-m', 'vendors.postgres.create_db_base_backup'])

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
        ]
