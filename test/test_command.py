from unittest import TestCase
from unittest.mock import patch

from command import WriteCommand, FullWriteCommand


class TestCommand(TestCase):
    @patch('subprocess.run')
    def test_write_command_run(self, mock_run):
        index = 3
        value = "0xAAAABBBB"
        write_command = WriteCommand(index, value)

        write_command.run()

        mock_run.assert_called_once_with(["python", "ssd.py", "W", index, value])

    @patch('subprocess.run')
    def test_full_write_command_run(self, mock_run):
        value = "0xAAAABBBB"
        full_write_command = FullWriteCommand(value)

        full_write_command.run()

        self.assertTrue(mock_run.call_count, 100)

