import unittest

from pathlib import Path

from db_rewind.postgres.config_file_handler.commands.disable_directive_command import DisableDirectiveCommand
from db_rewind.postgres.config_file_handler.commands.enable_directive_command import EnableDirectiveCommand
from db_rewind.postgres.config_file_handler.commands.set_directive_value_command import SetDirectiveValueCommand
from db_rewind.postgres.config_file_handler.file_handler import FileHandler
from db_rewind.postgres.config_file_handler.file_io import FileIO

THIS_DIR = Path(__file__).parent


class TestFileHandler(unittest.TestCase):
    def test_adding_setup_to_postgres_conf_file(self):
        file_path = THIS_DIR / 'fixtures/postgres.conf'
        file_io = FileIO(file_path)
        file_handler = FileHandler(file_io=file_io)

        file_handler.apply_command(SetDirectiveValueCommand('archive_mode', 'on'))

        file_handler.apply_command(SetDirectiveValueCommand('archive_command',
                                                            'test ! -f /var/lib/postgresql/wal_backup_12/%f && cp %p /var/lib/postgresql/wal_backup_12/%f',
                                                            True))

        file_handler.apply_command(SetDirectiveValueCommand('wal_level', 'archive'))

        # Enable disabled directive
        file_handler.apply_command(EnableDirectiveCommand('enable_async_append'))

        # Disable enabled directive
        file_handler.apply_command(DisableDirectiveCommand('exit_on_error'))

        # Enable already enabled directive
        file_handler.apply_command(EnableDirectiveCommand('archive_mode'))

        # Disable already disabled directive
        file_handler.apply_command(DisableDirectiveCommand('include_dir'))

        # Disable missing directive
        file_handler.apply_command(DisableDirectiveCommand('missing_directive'))

        # Enable missing directive
        file_handler.apply_command(EnableDirectiveCommand('missing_directive'))

        # Add new command to the end of the file
        file_handler.apply_command(SetDirectiveValueCommand('new_test_command', 'Yes', use_single_quotation=True))
        file_handler.apply_command(SetDirectiveValueCommand('new_test_command_2', 'No', use_single_quotation=False))

        in_memory_file = file_handler.save(in_memory=True)

        with open(THIS_DIR / 'fixtures/expected_postgres.conf') as expected:
            expected_file = expected.readlines()

        for line1, line2 in zip(in_memory_file, expected_file):
            self.assertEqual(line1, line2)

        self.assertEqual(len(in_memory_file), len(expected_file), f"{in_memory_file}\n\n{expected_file}")
