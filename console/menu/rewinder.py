import subprocess
import sys
from typing import List

from prompt_toolkit import PromptSession

from console.component.command import Command
from console.component.menu import Menu


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
        subprocess.run([sys.executable, '-m', 'vendors.postgres.db_server_manager', 'stop'])

    @staticmethod
    def start_postgres_server():
        subprocess.run([sys.executable, '-m', 'vendors.postgres.db_server_manager', 'start'])

    @staticmethod
    def destroy_db_data():
        subprocess.run([sys.executable, '-m', 'vendors.postgres.destroy_db_data'])

    @staticmethod
    def restore_db_base_backup():
        subprocess.run([sys.executable, '-m', 'vendors.postgres.restore_db_base_backup'])

    @staticmethod
    def create_recovery_signal_file():
        subprocess.run([sys.executable, '-m', 'vendors.postgres.create_recovery_signal_file'])

    @staticmethod
    def set_db_rewind_date(db_rewind_date: str):
        subprocess.run([sys.executable, '-m', 'vendors.postgres.set_db_rewind_date', db_rewind_date])

    @staticmethod
    def archive_wal_files():
        subprocess.run([sys.executable, '-m', 'vendors.postgres.archive_wal_files'])

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
