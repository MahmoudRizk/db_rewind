import unittest
import difflib

from pathlib import Path

from vendors.postgres.config_file_handler.file_handler import FileHandler

THIS_DIR = Path(__file__).parent

class TestFileHandler(unittest.TestCase):
    def test_adding_setup_to_postgres_conf_file(self):
        file_handler = FileHandler(THIS_DIR / 'fixtures/postgres.conf')

        file_handler.set_directive_value('archive_mode', 'on')
        file_handler.set_directive_value('archive_command', "test ! -f /var/lib/postgresql/wal_backup_12/%f && cp %p /var/lib/postgresql/wal_backup_12/%f", True)
        file_handler.set_directive_value('wal_level', 'archive')

        in_memory_file = file_handler.save(in_memory=True)

        with open(THIS_DIR / 'fixtures/expected_postgres.conf') as expected:
            expected_file = expected.readlines()

        for it1, it2 in zip(in_memory_file, expected_file):
            # print(it1, it2)
            self.assertEqual(it1, it2)
