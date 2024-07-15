import subprocess
import sys
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def run(self, *args):
        raise NotImplementedError


class ReadCommand(Command):
    def run(self):
        print("ReadCommand.run()")
        subprocess.run(["python", "ssd.py", "R", "0", "0x0"])


class ExitCommand(Command):
    def run(self):
        print("ExitCommand.run()")
        sys.exit()


class WriteCommand(Command):
    def __init__(self, index: int, value: str):
        self.__index = index
        self.__value = value

    def run(self):
        print("WriteCommand.run()")
        subprocess.run(["python", "ssd.py", "W", self.__index, self.__value])


class FullWriteCommand(Command):

    def __init__(self, value: str):
        self.__value = value

    def run(self):
        print("FullWriteCommand.run()")
        for index in range(100):
            write_command = WriteCommand(index, self.__value)
            write_command.run()
