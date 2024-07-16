from unittest import TestCase

from shell import Shell


class TestShell(TestCase):
    def setUp(self):
        self.shell = Shell()

    def test_parse_command_without_command(self):
        with self.assertRaises(ValueError):
            self.shell.parse_command("")

    def test_parse_command_with_invalid_command(self):
        with self.assertRaises(ValueError):
            self.shell.parse_command("hdd R 1")

    def test_parse_command_with_valid_read_and_write_commands(self):
        try:
            self.shell.parse_command("ssd R 1")
            self.shell.parse_command("ssd R 11")
            self.shell.parse_command("ssd W 1 0x00000000")
            self.shell.parse_command("ssd W 11 0xFFFFFFFF")
        except ValueError:
            self.fail()

    def test_parse_command_with_invalid_read_and_write_commands(self):
        with self.assertRaises(ValueError):
            self.shell.parse_command("ssd R")
        with self.assertRaises(ValueError):
            self.shell.parse_command("ssd R 0x1")
        with self.assertRaises(ValueError):
            self.shell.parse_command("ssd R -1")
        with self.assertRaises(ValueError):
            self.shell.parse_command("ssd R 100")
        with self.assertRaises(ValueError):
            self.shell.parse_command("ssd W")
        with self.assertRaises(ValueError):
            self.shell.parse_command("ssd W 1234567890")
        with self.assertRaises(ValueError):
            self.shell.parse_command("ssd W 0xXXXXXXXX")

    def test_help_and_exit_commands(self):
        try:
            self.shell.parse_command("help")
            self.shell.parse_command("exit")
        except ValueError:
            self.fail()
