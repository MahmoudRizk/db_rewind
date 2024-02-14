from multiprocessing import Process

from typing import List

from prompt_toolkit import PromptSession

from console.component.command import Command
from console.component.menu import Menu
from vendors.postgres.archive_wal_files import ArchiveWalFiles
from vendors.postgres.config_file_setup import ConfigFileSetup
from vendors.postgres.create_db_base_backup import CreateDBBaseBackup
from vendors.postgres.db_server_manager import DBServerManager


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
        p = Process(target=ConfigFileSetup.execute)
        p.start()
        p.join()

    @staticmethod
    def restart_postgres_server():
        p = Process(target=DBServerManager.execute, args=('restart',))
        p.start()
        p.join()

    @staticmethod
    def archive_wal_files():
        p = Process(target=ArchiveWalFiles.execute)
        p.start()
        p.join()

    @staticmethod
    def create_db_base_backup():
        p = Process(target=CreateDBBaseBackup.execute)
        p.start()
        p.join()

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
