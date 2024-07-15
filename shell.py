import subprocess

from command import Command, ReadCommand
from console import Console


class Shell:
    def __init__(self):
        self.console = Console()

    def run(self):
        while True:
            input()
            command = self.parse_command()
            command.run()
            self.console.read()

    def parse_command(self) -> Command:
        print("Shell.parse_command()")
        return ReadCommand()


if __name__ == "__main__":
    shell = Shell()
    shell.run()
