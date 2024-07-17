import subprocess
import sys
from abc import ABC, abstractmethod

from console import Console
from constant import *


class Command(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_command_type():
        pass

    def __init__(self, data1: str or None, data2: str or None):
        pass


class ReadCommand(Command):
    @staticmethod
    def get_command_type():
        return "read"

    def __init__(self, data1: str, data2: str or None):
        super().__init__(data1, data2)
        self.index = data1
        self.value = data2
        self.console = Console()

    def run(self):
        subprocess.run(["python", "ssd.py", "R", self.index])
        self.console.read()


class FullReadCommand(Command):
    @staticmethod
    def get_command_type():
        return "fullread"

    def __init__(self, data1: str or None, data2: str or None):
        super().__init__(data1, data2)

    def run(self):
        for index in range(NUM_LBA):
            read_command = ReadCommand(str(index))
            read_command.run()


class WriteCommand(Command):
    @staticmethod
    def get_command_type():
        return "write"

    def __init__(self, data1: str, data2: str):
        super().__init__(data1, data2)
        self.__index = data1
        self.__value = data2

    def run(self):
        subprocess.run(["python", "ssd.py", "W", self.__index, self.__value])


class FullWriteCommand(Command):

    @staticmethod
    def get_command_type():
        return "fullwrite"

    def __init__(self, data1: str or None, data2: str or None):
        super().__init__(data1, data2)
        self.__value = data1

    def run(self):
        for index in range(NUM_LBA):
            write_command = WriteCommand(str(index), self.__value)
            write_command.run()


class ExitCommand(Command):
    @staticmethod
    def get_command_type():
        return "exit"

    def run(self):
        sys.exit()


class HelpCommand(Command):

    @staticmethod
    def get_command_type():
        return "help"

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


class EraseCommand(Command):

    @staticmethod
    def get_command_type():
        return "erase"

    def __init__(self, data1, data2):
        super().__init__(data1, data2)
        self.lba = int(data1)
        self.size = int(data2)

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
    @staticmethod
    def get_command_type():
        return "erase_range"

    def __init__(self, data1, data2):
        super().__init__(data1, data2)
        self.start_lba = int(data1)
        self.end_lba = int(data2)

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
