from command import Command
from constant import *


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
            cmd, lba, data = entry[0], int(entry[1]), entry[2]
            if cmd == "E":
                data = int(data)
            buffer[i] = {"cmd": cmd, "lba": lba, "data": data}
        return buffer

    def add(self, command: Command) -> None:
        pass  # TODO: convert Command object to BufferEntry Object and append to self.__buffer

    def flush(self) -> None:
        # TODO: flush and update SSD
        for cmd_lst in self.__buffer:
            cmd_type = cmd_lst[0]

    def check_if_read_available(self, lba: int) -> bool:
        pass  # TODO: check if readable from buffer
