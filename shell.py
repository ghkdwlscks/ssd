import re

from command import Command, make_command
from console import Console


class Shell:
    def __init__(self):
        self.console = Console()

    def run(self):
        while True:
            try:
                command = self.parse_command(input())
            except ValueError:
                print("INVALID COMMAND")
                continue
            command.run()
            self.console.read()

    @staticmethod
    def parse_command(command: str) -> Command:
        if re.fullmatch(r"ssd R [0-9]{1,2}", command):
            return make_command(command)
        if re.fullmatch(r"ssd W [0-9]{1,2} 0x[0-9A-F]{8}", command):
            return make_command(command)
        if command == "help":
            return make_command(command)
        if command == "exit":
            return make_command(command)
        raise ValueError


if __name__ == "__main__":
    shell = Shell()
    shell.run()
