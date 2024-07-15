from unittest import TestCase
from unittest.mock import patch

from command import WriteCommand


class TestCommand(TestCase):
    @patch('subprocess.run')
    def test_write_run(self, mock_run):
        lba = "3"
        value = "0xAAAABBBB"
        write_command = WriteCommand()

        result = write_command.run(lba, value)

        mock_run.assert_called_once_with(["python", "ssd.py", "W", lba, value])
