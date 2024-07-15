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
        subprocess.run(["python", "ssd.py", "R", self.index])


class FullReadCommand(Command):
    def run(self):
        subprocess.run(["python", "ssd.py", "FR"])


class ExitCommand(Command):
    def run(self):
        sys.exit()
