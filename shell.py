import re

from command import Command, make_command
from test_app import TestApp, make_test_app


class Shell:

    def run(self):
        while True:
            try:
                command = self.parse_command(input("$ "))
            except ValueError:
                print("INVALID COMMAND")
                continue
            command.run()

    def parse_command(self, command: str) -> Command or TestApp:
        command = command.strip()
        if self.is_ssd_command(command):
            return make_command(command)
        if self.is_test_command(command):
            return make_test_app(command)
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
        return False

    @staticmethod
    def is_test_command(command):
        return command in ["testapp1", "testapp2"]


if __name__ == "__main__":
    shell = Shell()
    shell.run()
