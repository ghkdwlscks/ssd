from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from command import WriteCommand, FullWriteCommand, HelpCommand, ReadCommand, FullReadCommand

INDEX_0 = "0"
INDEX_10 = "10"
TEST_VALUE = "0xAAAABBBB"


class TestCommand(TestCase):

    def setUp(self):
        self.command = None

    @patch('subprocess.run')
    def test_read_index_0(self, mock_run):
        self.command = ReadCommand(INDEX_0)
        self.command.run()
        mock_run.assert_called_once_with(["python", 'ssd.py', 'R', INDEX_0])

    @patch('subprocess.run')
    def test_read_index_10(self, mock_run):
        self.command = ReadCommand(INDEX_10)
        self.command.run()
        mock_run.assert_called_once_with(["python", 'ssd.py', 'R', INDEX_10])

    @patch('subprocess.run')
    def test_fullread(self, mock_run):
        self.command = FullReadCommand()
        self.command.run()
        mock_run.assert_called_once_with(["python", 'ssd.py', 'FR'])

    @patch('subprocess.run')
    def test_write_command_run(self, mock_run):
        self.command = WriteCommand(INDEX_10, TEST_VALUE)

        self.command.run()

        mock_run.assert_called_once_with(["python", "ssd.py", "W", INDEX_10, TEST_VALUE])

    @patch('subprocess.run')
    def test_full_write_command_run(self, mock_run):
        self.command = FullWriteCommand(TEST_VALUE)

        self.command.run()

        self.assertEqual(100, mock_run.call_count)

    @patch('sys.stdout', new_callable=StringIO)
    def test_help_command_run(self, mock_stdout):
        expected_output = """
        - write: lba에 데이터를 기록합니다.
            write {{lba}} {{data}}

        - read: lba에 작성한 데이터를 읽습니다.
            read {{lba}}

        - exit: Shell을 종료합니다.

        - help: 도움말을 표시합니다.

        - fullwrite: 모든 lba에 해당 데이터를 기록합니다.
            fullwrite {{data}}

        - fullread: 모든 lba 데이터를 읽어 화면에 표시 합니다.
        """
        self.command = HelpCommand()

        self.command.run()

        self.assertEqual(expected_output.strip(), mock_stdout.getvalue().strip())
