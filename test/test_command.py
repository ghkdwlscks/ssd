from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from shell_command import WriteShellCommand, FullWriteShellCommand, HelpShellCommand, ReadShellCommand, FullReadShellCommand
from constant import *

class TestCommand(TestCase):

    def setUp(self):
        self.command = None

    @patch('subprocess.run')
    def test_read_index_0(self, mock_run):
        self.command = ReadShellCommand(INDEX_0)
        self.command.run()
        mock_run.assert_called_once_with(["python", 'ssd.py', 'R', INDEX_0])

    @patch('subprocess.run')
    def test_read_index_10(self, mock_run):
        self.command = ReadShellCommand(INDEX_10)
        self.command.run()
        mock_run.assert_called_once_with(["python", 'ssd.py', 'R', INDEX_10])

    @patch('subprocess.run')
    def test_fullread(self, mock_run):
        self.command = FullReadShellCommand()
        self.command.run()
        self.assertEqual(NUM_LBA, mock_run.call_count)

    @patch('subprocess.run')
    def test_write_command_run(self, mock_run):
        self.command = WriteShellCommand(INDEX_10, VALUE_0xAAAABBBB)

        self.command.run()

        mock_run.assert_called_once_with(["python", "ssd.py", "W", INDEX_10, VALUE_0xAAAABBBB])

    @patch('subprocess.run')
    def test_full_write_command_run(self, mock_run):
        self.command = FullWriteShellCommand(VALUE_0xAAAABBBB)

        self.command.run()

        self.assertEqual(NUM_LBA, mock_run.call_count)

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
    
    - flush: 버퍼의 command를 수행합니다.
    """
        self.command = HelpShellCommand()

        self.command.run()

        self.assertEqual(expected_output.strip(), mock_stdout.getvalue().strip())
