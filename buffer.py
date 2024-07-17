from abc import ABC

from command import Command
from constant import *


class BufferEntry(ABC):
    pass


class ReadEntry(BufferEntry):
    pass


class WriteEntry(BufferEntry):
    pass


class EraseEntry(BufferEntry):
    pass


class Buffer:
    def __init__(self):
        self.__buffer = self.load()

    @staticmethod
    def load() -> list[list[str]]:
        try:
            with open("buffer.txt", 'r') as file:
                buffer = [line.strip().split() for line in file]
        except FileNotFoundError:
            return []
        return buffer

    def add(self, command: Command) -> None:
        pass  # TODO: convert Command object to BufferEntry Object and append to self.__buffer

    def flush(self) -> None:
        # TODO: flush and update SSD
        for cmd_lst in self.__buffer:
            cmd_type = cmd_lst[0]

    def check_if_read_available(self, lba: int) -> bool:
        pass  # TODO: check if readable from buffer
