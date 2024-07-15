from unittest import TestCase
from unittest.mock import Mock

from console import Console
from ssd import SSD

RESULT_FILE = '../output/result.txt'
NAND_FILE = '../output/nand.txt'


class TestSSD(TestCase):
    def setUp(self):
        self.sut = SSD()

    def test_ssd_set_command(self):
        self.sut.set_command('R', 5)

    def test_ssd_set_command_fail_out_of_lba_range(self):
        with self.assertRaises(AttributeError):
            self.sut.set_command('R', 100)

    def test_ssd_set_command_wrong_cmd(self):
        with self.assertRaises(AttributeError):
            self.sut.set_command('Read', 5)

    def test_ssd_read_empty_nand(self):
        self.refresh_nand()
        self.sut.set_command('R', 5)
        self.sut.run()

    def test_ssd_write(self):
        self.refresh_nand()
        self.sut.set_command('W', 5, "0xAB010105")
        self.run()

        self.assertEqual('0xAB010105', self.check_nand_txt(5))

    def test_ssd_write_and_read(self):
        self.refresh_nand()
        self.sut.set_command('W', 5, "0xAB010105")
        self.sut.run()

        self.sut.set_command('R', 5)
        self.sut.run()

        with open(RESULT_FILE, 'r') as f:
            content = f.readline()
            lba, data = content.split()
        self.assertEqual(5, lba)
        self.assertEqual("0xAB010105", data)
