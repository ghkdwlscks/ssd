import os
from unittest import TestCase
from unittest.mock import Mock

from ssd import SSD
from constant import *


FULL_READ_FILE = '\n'.join([VALUE_DEFAULT for _ in range(NUM_LBA)])

class TestSSD(TestCase):
    def setUp(self):
        os.environ['NAND_TXT_PATH'] = 'output\\nand_test.txt'
        os.environ['RESULT_TXT_PATH'] = 'output\\result_test.txt'
        self.sut = SSD()
        self.nand_txt_file = Mock()
        self.result_txt_file = Mock()

    def tearDown(self):
        if NAND_TXT_PATH in os.environ:
            del os.environ[NAND_TXT_PATH]
        if RESULT_TXT_PATH in os.environ:
            del os.environ[RESULT_TXT_PATH]

    def test_ssd_set_command(self):
        self.sut.set_command(CMD_R, INT_INDEX_5)

    def test_ssd_set_command_fail_out_of_lba_range(self):
        with self.assertRaises(AttributeError):
            self.sut.set_command(CMD_R, NUM_LBA)

    def test_ssd_set_command_wrong_cmd(self):
        with self.assertRaises(AttributeError):
            self.sut.set_command('Read', INT_INDEX_5)

    def test_ssd_read_empty_nand(self):
        self.sut.refresh_nand()
        self.sut.set_command(CMD_R, INT_INDEX_5)
        self.sut.run()
        self.result_txt_file.return_value = VALUE_DEFAULT

        self.assertEqual(VALUE_DEFAULT, self.result_txt_file())

    def test_ssd_write(self):
        self.sut.refresh_nand()
        self.sut.set_command(CMD_W, INT_INDEX_5, VALUE_0xAB010105)
        self.sut.run()
        self.nand_txt_file.side_effect = lambda x: VALUE_0xAB010105 if x == INT_INDEX_5 else VALUE_DEFAULT

        self.assertEqual(VALUE_0xAB010105, self.nand_txt_file(INT_INDEX_5))

    def test_ssd_write_and_read(self):
        self.sut.refresh_nand()
        self.sut.set_command(CMD_W, INT_INDEX_5, VALUE_0xAB010105)
        self.sut.run()
        self.nand_txt_file.side_effect = lambda x: VALUE_0xAB010105 if x == INT_INDEX_5 else VALUE_DEFAULT

        self.sut.set_command(CMD_R, INT_INDEX_5)
        self.sut.run()
        self.result_txt_file.return_value = VALUE_0xAB010105

        self.assertEqual(VALUE_0xAB010105, self.result_txt_file())

    def test_full_read(self):
        self.sut.refresh_nand()
        self.result_txt_file.return_value = FULL_READ_FILE
        self.sut.full_read()
        self.assertEqual(FULL_READ_FILE, self.result_txt_file())
