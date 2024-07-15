from unittest import TestCase
from unittest.mock import Mock, patch
from command import ReadCommand, FullReadCommand
from ssd import SSD
from shell import Shell

INDEX_0 = 0
INDEX_10 = 10


class TestCommandRead(TestCase):
    @patch('subprocess.run')
    def test_read_index_0(self, mock_run):
        read_command = ReadCommand(INDEX_0)
        read_command.run()
        mock_run.assert_called_once_with(["python", 'ssd.py', 'R', INDEX_0])

    @patch('subprocess.run')
    def test_read_index_10(self, mock_run):
        read_command = ReadCommand(INDEX_10)
        read_command.run()
        mock_run.assert_called_once_with(["python", 'ssd.py', 'R', INDEX_10])

    @patch('subprocess.run')
    def test_fullread(self, mock_run):
        fullread_command = FullReadCommand()
        fullread_command.run()
        self.assertEqual(100, mock_run.call_count)
