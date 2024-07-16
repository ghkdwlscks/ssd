import os
from unittest import TestCase
from unittest.mock import Mock

from ssd import SSD


class TestSSD(TestCase):
    def setUp(self):
        os.environ['NAND_TXT_PATH'] = 'output\\nand_test.txt'
        os.environ['RESULT_TXT_PATH'] = 'output\\result_test.txt'
        self.sut = SSD()
        self.nand_txt_file = Mock()
        self.result_txt_file = Mock()

    def tearDown(self):
        if 'NAND_TXT_PATH' in os.environ:
            del os.environ['NAND_TXT_PATH']
        if 'RESULT_TXT_PATH' in os.environ:
            del os.environ['RESULT_TXT_PATH']

    def test_ssd_set_command(self):
        self.sut.set_command('R', 5)

    def test_ssd_set_command_fail_out_of_lba_range(self):
        with self.assertRaises(AttributeError):
            self.sut.set_command('R', 100)

    def test_ssd_set_command_wrong_cmd(self):
        with self.assertRaises(AttributeError):
            self.sut.set_command('Read', 5)

    def test_ssd_read_empty_nand(self):
        self.sut.refresh_nand()
        self.sut.set_command('R', 5)
        self.sut.run()
        self.result_txt_file.return_value = '0x00000000'

        self.assertEqual('0x00000000', self.result_txt_file())

    def test_ssd_write(self):
        self.sut.refresh_nand()
        self.sut.set_command('W', 5, "0xAB010105")
        self.sut.run()
        self.nand_txt_file.side_effect = lambda x: '0xAB010105' if x == 5 else '0x00000000'

        self.assertEqual('0xAB010105', self.nand_txt_file(5))

    def test_ssd_write_and_read(self):
        self.sut.refresh_nand()
        self.sut.set_command('W', 5, "0xAB010105")
        self.sut.run()
        self.nand_txt_file.side_effect = lambda x: '0xAB010105' if x == 5 else '0x00000000'

        self.sut.set_command('R', 5)
        self.sut.run()
        self.result_txt_file.return_value = '0xAB010105'

        self.assertEqual("0xAB010105", self.result_txt_file())
