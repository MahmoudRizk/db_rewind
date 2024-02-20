from typing import List

from prompt_toolkit import PromptSession

from console.component.command import Command
from console.component.menu import Menu
from vendors.postgres.procedures.archive_wal_files import ArchiveWalFiles
from vendors.postgres.procedures.config_file_setup import ConfigFileSetup
from vendors.postgres.procedures.create_db_base_backup import CreateDBBaseBackup
from vendors.postgres.procedures.db_server_manager import DBServerManager


class Setup(Menu):
    def __init__(self, session: PromptSession):
        super().__init__(session=session, prompt_name='setup')

    @staticmethod
    def install() -> None:
        Setup.configure_postgres_conf_file()
        Setup.restart_postgres_server()

        Setup.archive_wal_files()
        Setup.create_db_base_backup()

    @staticmethod
    def configure_postgres_conf_file():
        ConfigFileSetup().execute()

    @staticmethod
    def restart_postgres_server():
        DBServerManager('restart').execute()

    @staticmethod
    def archive_wal_files():
        ArchiveWalFiles().execute()

    @staticmethod
    def create_db_base_backup():
        CreateDBBaseBackup().execute()

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
