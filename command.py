import subprocess
import sys
from abc import ABC, abstractmethod
from console import Console
from constant import *
from logger import Logger



class Command(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError


class ReadCommand(Command):
    def __init__(self, index: str):
        self.index = index
        self.console = Console()
        self.logger = Logger()

    def run(self):
        self.logger.log(self, "run()", "ReadCommand 실행")
        subprocess.run(["python", "ssd.py", "R", self.index])
        self.console.read()


class FullReadCommand(Command):

    def __init__(self):
        self.logger = Logger()

    def run(self):
        self.logger.log(self, "run()", "FullReadCommand 실행")
        for index in range(NUM_LBA):
            read_command = ReadCommand(str(index))
            read_command.run()


class WriteCommand(Command):
    def __init__(self, index: str, value: str):
        self.logger = Logger()
        self.__index = index
        self.__value = value

    def run(self):
        self.logger.log(self, "run()", "WriteCommand 실행")
        subprocess.run(["python", "ssd.py", "W", self.__index, self.__value])


class FullWriteCommand(Command):

    def __init__(self, value: str):
        self.__value = value
        self.logger = Logger()

    def run(self):
        for index in range(NUM_LBA):
            self.logger.log(self, "run()", "FullWriteCommand 실행")
            write_command = WriteCommand(str(index), self.__value)
            write_command.run()


class ExitCommand(Command):
    def __init__(self):
        self.logger = Logger()

    def run(self):
        self.logger.log(self, "run()", "exit 실행")
        sys.exit()


class HelpCommand(Command):
    def __init__(self):
        self.logger = Logger()

    def run(self):
        self.logger.log(self, "run()", "help 실행")
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


class EraseCommand(Command):

    def __init__(self, _lba, _size):
        self.lba = int(_lba)
        self.size = int(_size)

    def run(self):
        if self.size <= 10:
            subprocess.run(["python", "ssd.py", "E", str(self.lba), str(self.size)])
            return

        left_size = self.size
        start_address = self.lba
        while left_size // 10:
            subprocess.run(["python", "ssd.py", "E", str(start_address), str(10)])
            start_address += 10
            left_size -= 10
        subprocess.run(["python", "ssd.py", "E", str(start_address), str(left_size)])


class EraseRangeCommand(Command):
    def __init__(self, _start_lba, _end_lba):
        self.start_lba = int(_start_lba)
        self.end_lba = int(_end_lba)

    def run(self):
        if self.end_lba <= self.start_lba:
            return
        left_size = self.end_lba - self.start_lba
        start_address = self.start_lba
        if left_size <= 10:
            subprocess.run(["python", "ssd.py", "E", str(self.start_lba), str(left_size)])
            return

        while left_size // 10:
            subprocess.run(["python", "ssd.py", "E", str(start_address), str(10)])
            start_address += 10
            left_size -= 10
        subprocess.run(["python", "ssd.py", "E", str(start_address), str(left_size)])


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
    if command_type == "erase":
        return EraseCommand(command[1], command[2])
    if command_type == "erase_range":
        return EraseRangeCommand(command[1], command[2])
