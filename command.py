import subprocess
import sys
from abc import ABC, abstractmethod

from console import Console
from constant import *

class Command(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError


class ReadCommand(Command):
    def __init__(self, index: str):
        self.index = index
        self.console = Console()

    def run(self):
        subprocess.run(["python", "ssd.py", "R", self.index])
        self.console.read()


class FullReadCommand(Command):
    def run(self):
        for index in range(NUM_LBA):
            read_command = ReadCommand(str(index))
            read_command.run()


class WriteCommand(Command):
    def __init__(self, index: str, value: str):
        self.__index = index
        self.__value = value

    def run(self):
        subprocess.run(["python", "ssd.py", "W", self.__index, self.__value])


class FullWriteCommand(Command):

    def __init__(self, value: str):
        self.__value = value

    def run(self):
        for index in range(NUM_LBA):
            write_command = WriteCommand(str(index), self.__value)
            write_command.run()


class ExitCommand(Command):
    def run(self):
        sys.exit()


class HelpCommand(Command):

    def run(self):
        print("""
        - write: lba에 데이터를 기록합니다.
            write {{lba}} {{data}}

        - read: lba에 작성한 데이터를 읽습니다.
            read {{lba}}

        - exit: Shell을 종료합니다.

        - help: 도움말을 표시합니다.

        - fullwrite: 모든 lba에 해당 데이터를 기록합니다.
            fullwrite {{data}}

        - fullread: 모든 lba 데이터를 읽어 화면에 표시 합니다.
        """)


def make_command(command: str) -> Command:
    command = command.split()
    command_type = command[0]

    if command_type == "read":
        return ReadCommand(command[1])
    if command_type == 'write':
        return WriteCommand(command[1], command[2])
    if command_type == "help":
        return HelpCommand()
    if command_type == "exit":
        return ExitCommand()
    if command_type == "fullread":
        return FullReadCommand()
    if command_type == "fullwrite":
        return FullWriteCommand(command[1])
