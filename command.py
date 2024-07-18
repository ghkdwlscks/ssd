from abc import ABC, abstractmethod

from console import Console
from constant import *
from logger import Logger



class Command(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_command_type():
        pass


    def __init__(self, data1: str or None = None, data2: str or None = None):
        self.logger = Logger()
      