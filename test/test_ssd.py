import os
from unittest import TestCase
from unittest.mock import Mock

from console import Console
from ssd import SSD
from constant import *


class TestSSD(TestCase):
    def setUp(self):
        os.environ['NAND_TXT_PATH'] = 'output\\nand_test.txt'
        os.environ['RESULT_TXT_PATH'] = 'output\\result_test.txt'
        self.sut = SSD()
        self.nand_txt_file = Mock()
        self.console = Mock(spec=Console())
        self.console.read.return_value = True
        self.nand_txt_file.side_effect = lambda x: VALUE_0xAB010105 if x == INT_INDEX_5 else VALUE_DEFAULT

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
        self.assertEqual(True, self.console.read())

    def test_ssd_write(self):
        self.sut.refresh_nand()
        self.sut.set_command(CMD_W, INT_INDEX_5, VALUE_0xAB010105)
        self.sut.run()

        self.assertEqual(VALUE_0xAB010105, self.nand_txt_file(INT_INDEX_5))

    def test_ssd_write_and_read(self):
        self.sut.refresh_nand()
        self.sut.set_command(CMD_W, INT_INDEX_5, VALUE_0xAB010105)
        self.sut.run()

        self.sut.set_command(CMD_R, INT_INDEX_5)
        self.sut.run()

        self.assertEqual(True, self.console.read())
