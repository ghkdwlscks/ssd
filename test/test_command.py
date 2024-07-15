from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from command import WriteCommand, FullWriteCommand, Command, HelpCommand


class TestCommand(TestCase):

    def setUp(self):
        self.command = None

    @patch('subprocess.run')
    def test_write_command_run(self, mock_run):
        index = 3
        value = "0xAAAABBBB"
        self.command = WriteCommand(index, value)

        self.command.run()

        mock_run.assert_called_once_with(["python", "ssd.py", "W", index, value])

    @patch('subprocess.run')
    def test_full_write_command_run(self, mock_run):
        value = "0xAAAABBBB"
        self.command = FullWriteCommand(value)

        self.command.run()

        self.assertTrue(mock_run.call_count, 100)

    def test_help_command_run(self):
        expected_output ="""
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
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.command.run()
            printed_output = fake_out.getvalue().strip()  # Get printed output and strip any extra whitespace

        self.assertEqual(printed_output, expected_output.strip())
