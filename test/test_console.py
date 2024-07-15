from unittest import TestCase
from unittest.mock import Mock

from console import Console


class TestConsole(TestCase):

    def setUp(self):
        self.sut = Console()

    # result.txt 파일이 없다고 가정; Mock 사용
    def test_try_to_read_nonexisting_result_file(self):
        self.sut.is_exist_result_file = Mock()
        self.sut.is_exist_result_file.return_value = False

        self.assertFalse(self.sut.read())

    def test_read_and_print(self):
        self.sut.is_exist_result_file = Mock()
        self.sut.is_exist_result_file.return_value = True

        self.sut.read_result_file = Mock()
        mock_value = [(x, f'0x32{x}') for x in range(100)]
        self.sut.read_result_file.return_value = mock_value

        self.assertTrue(self.sut.read())
