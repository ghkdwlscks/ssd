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
    def run(self, *args):
        print("WriteCommand.run()")
        lba, value = args
        subprocess.run(["python", "ssd.py", "W", lba, value])
