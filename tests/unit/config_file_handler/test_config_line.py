import unittest
from parameterized import parameterized

from db_rewind.postgres.config_file_handler.config_line import ConfigLine


class TestConfigLine(unittest.TestCase):
    
    @parameterized.expand([
        ["#hba_file = 'ConfigDir/pg_hba.conf' # host-based authentication file", "#hba_file = 'ConfigDir/pg_hba.conf' # host-based authentication file"],
        ["hba_file = ''", "hba_file = ''"]
    ])
    def test_get_line(self, line: str, expected: str):
        config_line = ConfigLine(line)

        self.assertEqual(expected, config_line.get())
    
    @parameterized.expand([
        ["#hba_file = 'ConfigDir/pg_hba.conf' # host-based authentication file", "hba_file"],
        ["#hba_file = 'ConfigDir/pg_hba.conf'        # host-based authentication file        ", "hba_file"],
        ["hba_file = 'ConfigDir/pg_hba.conf' # host-based authentication file", "hba_file"],
        ["hba_file = 'ConfigDir/pg_hba.conf'", "hba_file"]
    ])
    def test_get_directive_name(self, line: str, expected: str):
        config_line = ConfigLine(line)
        self.assertEqual(expected, config_line.get_directive_name())
    
    @parameterized.expand([
        ["#hba_file = 'ConfigDir/pg_hba.conf' # host-based authentication file", "hba_file = 'ConfigDir/pg_hba.conf' # host-based authentication file"],
        ["hba_file = 'ConfigDir/pg_hba.conf' # host-based authentication file", "hba_file = 'ConfigDir/pg_hba.conf' # host-based authentication file"],
        ["hba_file = 'ConfigDir/pg_hba.conf'", "hba_file = 'ConfigDir/pg_hba.conf'"]
    ])
    def test_enable_directive(self, line: str, expected: str):
        config_line = ConfigLine(line)
        self.assertEqual(expected, config_line.enable_directive().get())
    
    @parameterized.expand([
        ["#hba_file = 'ConfigDir/pg_hba.conf' # host-based authentication file", "#hba_file = 'ConfigDir/pg_hba.conf' # host-based authentication file"],
        ["hba_file = 'ConfigDir/pg_hba.conf' # host-based authentication file", "#hba_file = 'ConfigDir/pg_hba.conf' # host-based authentication file"],
        ["hba_file = 'ConfigDir/pg_hba.conf'", "#hba_file = 'ConfigDir/pg_hba.conf'"]
    ])
    def test_disable_directive(self, line: str, expected: str):
        config_line = ConfigLine(line)
        self.assertEqual(expected, config_line.disable_directive().get()) 
    
    @parameterized.expand([
        ["#hba_file = 'ConfigDir/pg_hba.conf' # host-based authentication file", '/home/hba.conf', True, "hba_file = '/home/hba.conf' # host-based authentication file"],
        ["#hba_file = 'ConfigDir/pg_hba.conf'    # host-based authentication file    ", '/home/hba.conf', True, "hba_file = '/home/hba.conf'    # host-based authentication file    "],
        ["#hba_file = 'ConfigDir/pg_hba.conf'", '/home/hba.conf', True, "hba_file = '/home/hba.conf'"],
        ["#load_timeout = '0'", '123', False, "load_timeout = 123"],
        ["#load_timeout = 99", '456', False, "load_timeout = 456"],
    ])
    def test_set_directive_value(self, line: str, value: str, use_single_quotation: bool, expected: str):
        config_line = ConfigLine(line)
        self.assertEqual(expected, config_line.set_directive_value(value, use_single_quotation).get())
    

    @parameterized.expand([
        ["#hba_file = 'ConfigDir/pg_hba.conf' # host-based authentication file", "hba_file", True],
        ["hba_file = 'ConfigDir/pg_hba.conf' # host-based authentication file", "hba_file", True],
        ["hba_file = 'ConfigDir/pg_hba.conf'", "hba_file", True],
        ["#hba_file = 'ConfigDir/pg_hba.conf'", "hba_file", True],
    ])
    def test_has_directive(self, line: str, directive_name: str, expected: bool):
        config_line = ConfigLine(line)
        self.assertEqual(expected, config_line.has_directive(directive_name))        
    
    
