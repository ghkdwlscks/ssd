import subprocess
import sys
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError


class ReadCommand(Command):
    def __init__(self, index: int):
        self.index = index

    def run(self):
        print("ReadCommand.run()")
        subprocess.run(["python", "ssd.py", "R", self.index])


class FullReadCommand(Command):
    def run(self):
        print("FullReadCommand.run()")
        for index in range(100):
            subprocess.run(["python", "ssd.py", "R", index])


class ExitCommand(Command):
    def run(self):
        print("ExitCommand.run()")
        sys.exit()
