from command import Command, WriteCommand, EraseCommand
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

    def add(self, cmd, lba, data) -> None:
        entry = {"cmd": cmd, "lba": int(lba), "data": data}
        if cmd == "E":
            data = int(data)
        self.__buffer.append(entry)
        # TODO: Call optimize functions
        if len(self.__buffer) >= 10:
            self.flush()


    def flush(self) -> None:
        for cmd_lst in self.__buffer:
            cmd_type = cmd_lst[0]
            if cmd_type == CMD_W:
                WriteCommand(**cmd_lst[1:])
            elif cmd_type == CMD_E:
                EraseCommand(**cmd_lst[1:])
            else:
                ValueError("wrong command in buffer")

        # erase buffer.txt
        with open("output/buffer.txt", 'w') as file:
            file.write('')


    def check_if_read_available(self, lba: int) -> bool:
        pass  # TODO: check if readable from buffer
