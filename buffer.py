from abc import ABC

from command import Command


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

    def load(self) -> list[BufferEntry]:
        pass  # TODO: read buffer entries from buffer.txt and return entries

    def add(self, command: Command) -> None:
        pass  # TODO: convert Command object to BufferEntry Object and append to self.__buffer

    def flush(self) -> None:
        pass  # TODO: flush and update SSD

    def check_if_read_available(self, lba: int) -> bool:
        pass  # TODO: check if readable from buffer
