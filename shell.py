import re
import sys

from command import Command, make_command
from logger import Logger
from test_app import TestApp


class Shell:
    def __init__(self, run_list_file=None):
        self.run_list_file = run_list_file
        if not self.run_list_file:
            return
        with open(self.run_list_file) as file:
            self.scripts = [line.strip() for line in file]
        self.logger = Logger()

    def run(self):
        self.logger.log(self, "run()", "Shell 실행")
        while True:
            try:
                command = self.parse_command(input("$ "))
            except ValueError:
                print("INVALID COMMAND")
                self.logger.log(self, "run()", "INVALID COMMAND 발생")
                continue
            command.run()

    def parse_command(self, command: str) -> Command or TestApp:
        self.logger.log(self, "parse_command()", "command 파싱")
        command = command.strip()
        if self.is_ssd_command(command):
            return make_command(command)
        else:
            try:
                return TestApp(command)
            except FileNotFoundError:
                self.logger.log(self, "parse_command()", "파싱 실패 ValueError 발생")
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
        if re.fullmatch(r"erase [0-9]{1,2} \b(?:100|\d{1,2})\b$", command):
            return True
        if re.fullmatch(r"erase_range [0-9]{1,2} [0-9]{1,2}", command):
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
