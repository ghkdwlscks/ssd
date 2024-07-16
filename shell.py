import re

from command import Command, FullReadCommand, make_command, ReadCommand
from console import Console


class Shell:
    def __init__(self):
        self.console = Console()

    def run(self):
        while True:
            try:
                command = self.parse_command(input("$ "))
            except ValueError:
                print("INVALID COMMAND")
                continue
            command.run()
            if isinstance(command, (ReadCommand, FullReadCommand)):
                self.console.read()

    @staticmethod
    def parse_command(command: str) -> Command:
        if re.fullmatch(r"read [0-9]{1,2}", command):
            return make_command(command)
        if re.fullmatch(r"write [0-9]{1,2} 0x[0-9A-F]{8}", command):
            return make_command(command)
        if command == "help":
            return make_command(command)
        if command == "exit":
            return make_command(command)
        if command == "fullread":
            return make_command(command)
        if re.fullmatch(r"fullwrite 0x[0-9A-F]{8}", command):
            return make_command(command)

        raise ValueError


if __name__ == "__main__":
    shell = Shell()
    shell.run()
