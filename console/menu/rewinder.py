from typing import List

from prompt_toolkit import PromptSession

from console.component.command import Command
from console.component.menu import Menu
from vendors.postgres.procedures.archive_wal_files import ArchiveWalFiles
from vendors.postgres.procedures.create_recovery_signal_file import CreateRecoverySignalFile
from vendors.postgres.procedures.db_server_manager import DBServerManager
from vendors.postgres.procedures.destroy_db_data import DestroyDBData
from vendors.postgres.procedures.restore_db_base_backup import RestoreDBBaseBackup
from vendors.postgres.procedures.set_db_rewind_date import SetDBRewindDate


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
        res = DBServerManager(command='stop').execute()
        # print(res.as_dict())

    @staticmethod
    def start_postgres_server():
        res = DBServerManager(command='start').execute()
        # print(res.as_dict())

    @staticmethod
    def destroy_db_data():
        res = DestroyDBData().execute()
        print(res.as_dict())

    @staticmethod
    def restore_db_base_backup():
        res = RestoreDBBaseBackup().execute()
        print(res.as_dict())

    @staticmethod
    def create_recovery_signal_file():
        res = CreateRecoverySignalFile().execute()
        print(res.as_dict())

    @staticmethod
    def set_db_rewind_date(db_rewind_date: str):
        res = SetDBRewindDate(db_rewind_date=db_rewind_date).execute()
        # print(res.as_dict())

    @staticmethod
    def archive_wal_files():
        res = ArchiveWalFiles().execute()
        print(res.as_dict())

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
