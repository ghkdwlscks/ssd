import sys

from shell_command import ShellCommand
from command_factory import ShellCommandFactory
from logger import Logger
from test_app import TestApp
from utils import is_ssd_command


class Shell:
    def __init__(self, run_list_file=None):
        self.run_list_file = run_list_file
        self.logger = Logger()
        if not self.run_list_file:
            return
        with open(self.run_list_file) as file:
            self.scripts = [line.strip() for line in file]

    def run(self):
        self.logger.log("Shell 실행")
        while True:
            try:
                command = self.parse_command(input("$ "))
            except ValueError:
                print("INVALID COMMAND")
                self.logger.log("INVALID COMMAND 발생")
                continue
            command.run()

    def parse_command(self, command: str) -> ShellCommand or TestApp:
        self.logger.log("command 파싱")
        command = command.strip()
        if is_ssd_command(command):
            return ShellCommandFactory(command).create_command()
        else:
            try:
                return TestApp(command)
            except FileNotFoundError:
                self.logger.log("파싱 실패 ValueError 발생")
                raise ValueError


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
