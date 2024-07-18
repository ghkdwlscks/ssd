import re
import sys

from shell_command import ShellCommand
from command_factory import ShellCommandFactory
from test_app import TestApp


class Shell:
    def __init__(self, run_list_file=None):
        self.run_list_file = run_list_file
        if not self.run_list_file:
            return
        with open(self.run_list_file) as file:
            self.scripts = [line.strip() for line in file]

    def run(self):
        while True:
            try:
                command = self.parse_command(input("$ "))
            except ValueError:
                print("INVALID COMMAND")
                continue
            command.run()

    def parse_command(self, command: str) -> ShellCommand or TestApp:
        command = command.strip()
        if self.is_ssd_command(command):
            return ShellCommandFactory(command).create_command()
        else:
            try:
                return TestApp(command)
            except FileNotFoundError:
                raise ValueError

    @staticmethod
    def is_ssd_command(command):
        if command in ["help", "exit", "fullread"]:
            return True
        if re.fullmatch(r"read [0-9]{1,2}", command):
            return True
        if re.fullmatch(r"write [0-9]{1,2} 0x[0-9A-F]{8}", command):
            return True
        if re.fullmatch(r"fullwrite 0x[0-9A-F]{8}", command):
            return True
        if re.fullmatch(r"(erase|erase_range) [0-9]{1,2} \b(?:100|\d{1,2})\b$", command):
            return True
        return False

    @staticmethod
    def is_test_command(command):
        return command in ["testapp1", "testapp2"]

    def run_scripts(self):
        for script in self.scripts:
            try:
                test_app = TestApp(script)
                if not test_app.run():
                    sys.exit(1)
            except FileNotFoundError:
                sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        shell = Shell()
        shell.run()
    elif len(sys.argv) == 2:
        shell = Shell(sys.argv[1])
        shell.run_scripts()
