from io import StringIO
from unittest import TestCase
from unittest.mock import Mock, patch

from console import Console
from constant import *

class TestConsole(TestCase):

    def setUp(self):
        self.sut = Console()

    # result.txt 파일이 없다고 가정; Mock 사용
    def test_try_to_read_nonexisting_result_file(self):
        self.sut.is_exist_result_file = Mock()
        self.sut.is_exist_result_file.return_value = False

        self.assertEqual(self.sut.read(), None)

    @patch('builtins.print')
    def test_read_print_output(self, mock_print):
        # Mock 설정
        self.sut.is_exist_result_file = Mock(return_value=True)
        mock_value = VALUE_0x32991111
        self.sut.read_result_file = Mock(return_value=mock_value)
        self.sut.read()

        mock_print.assert_called_once_with(mock_value)
