import subprocess
import sys
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError


class ReadCommand(Command):
    def run(self):
        print("ReadCommand.run()")
        subprocess.run(["python", "ssd.py", "R", "0", "0x0"])


class ExitCommand(Command):
    def run(self):
        print("ExitCommand.run()")
        sys.exit()
