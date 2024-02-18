from typing import List

from prompt_toolkit import PromptSession

from console.component.command import Command
from console.component.menu import Menu
from vendors.postgres.archive_wal_files import ArchiveWalFiles
from vendors.postgres.create_recovery_signal_file import CreateRecoverySignalFile
from vendors.postgres.db_server_manager import DBServerManager
from vendors.postgres.destroy_db_data import DestroyDBData
from vendors.postgres.restore_db_base_backup import RestoreDBBaseBackup
from vendors.postgres.set_db_rewind_date import SetDBRewindDate


class Rewinder(Menu):
    def __init__(self, session: PromptSession):
        super().__init__(session=session, prompt_name='DBRewinder')

    def rewind(self):
        print('Please enter date time to rewind to in format YYYY-mm-dd HH:MM:SS :')
        date_time = self.session.prompt("")

        Rewinder.archive_wal_files()
        Rewinder.stop_postgres_server()
        Rewinder.destroy_db_data()
        Rewinder.restore_db_base_backup()

        Rewinder.create_recovery_signal_file()
        Rewinder.set_db_rewind_date(date_time)
        Rewinder.start_postgres_server()

    @staticmethod
    def stop_postgres_server():
        DBServerManager.execute('stop')

    @staticmethod
    def start_postgres_server():
        DBServerManager.execute('start')

    @staticmethod
    def destroy_db_data():
        DestroyDBData.execute()

    @staticmethod
    def restore_db_base_backup():
        RestoreDBBaseBackup.execute()

    @staticmethod
    def create_recovery_signal_file():
        CreateRecoverySignalFile.execute()

    @staticmethod
    def set_db_rewind_date(db_rewind_date: str):
        SetDBRewindDate.execute(db_rewind_date)

    @staticmethod
    def archive_wal_files():
        ArchiveWalFiles.execute()

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
