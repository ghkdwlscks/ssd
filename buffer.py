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
    def load() -> list[dict]:
        try:
            with open("output/buffer.txt", 'r') as file:
                buffer = [line.strip().split() for line in file]
        except FileNotFoundError:
            return []
        for i, entry in enumerate(buffer):
            if entry[0] == "W":
                buffer[i] = {"cmd": "W", "addr": entry[1], "value": entry[2]}
            elif entry[0] == "E":
                buffer[i] = {"cmd": "E", "addr": entry[1:]}
            print(buffer[i])
        return buffer

    def add(self, command: Command) -> None:
        pass  # TODO: convert Command object to BufferEntry Object and append to self.__buffer

    def flush(self) -> None:
        # TODO: flush and update SSD
        for cmd_lst in self.__buffer:
            cmd_type = cmd_lst[0]

    def check_if_read_available(self, lba: int) -> bool:
        pass  # TODO: check if readable from buffer

buffer = Buffer()