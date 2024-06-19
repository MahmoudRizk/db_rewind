import unittest

from pathlib import Path

from db_rewind.postgres.config_file_handler.file_handler import FileHandler

THIS_DIR = Path(__file__).parent

class TestFileHandler(unittest.TestCase):
    def test_adding_setup_to_postgres_conf_file(self):
        file_handler = FileHandler(THIS_DIR / 'fixtures/postgres.conf')

        file_handler.set_directive_value('archive_mode', 'on')
        file_handler.set_directive_value('archive_command', "test ! -f /var/lib/postgresql/wal_backup_12/%f && cp %p /var/lib/postgresql/wal_backup_12/%f", True)
        file_handler.set_directive_value('wal_level', 'archive')

        # Enable disabled directive
        file_handler.enable_directive('enable_async_append')
        
        # Disable enabled directive
        file_handler.disable_directive('exit_on_error')

        # Enable already enabled directive
        file_handler.enable_directive('archive_mode')

        # Disable already disabled directive
        file_handler.disable_directive('include_dir')

        # Disable missing directive
        file_handler.disable_directive('missing_directive')

        # Enable missing directive
        file_handler.enable_directive('missing_directive')

        # Add new command to the end of the file
        file_handler.set_directive_value('new_test_command', 'Yes', use_single_quotation=True)
        file_handler.set_directive_value('new_test_command_2', 'No', use_single_quotation=False)

        in_memory_file = file_handler.save(in_memory=True)

        with open(THIS_DIR / 'fixtures/expected_postgres.conf') as expected:
            expected_file = expected.readlines()

        for line1, line2 in zip(in_memory_file, expected_file):
            self.assertEqual(line1, line2)

        self.assertEqual(len(in_memory_file), len(expected_file), f"{in_memory_file}\n\n{expected_file}")