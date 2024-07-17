from command import Command, WriteCommand, EraseCommand
from constant import *


class Buffer:
    def __init__(self):
        self.__buffer = self.load()
        print(self.__buffer)

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
        with open("output/buffer.txt", "w") as file:
            for entry in self.__buffer:
                file.write(f"{entry[0]} {entry[1]} {entry[2]}\n")


    def flush(self) -> None:
        for entry in self.__buffer:
            if entry['cmd'] == CMD_W:
                WriteCommand(str(entry["lba"]), entry["data"])
            elif entry['cmd'] == CMD_E:
                EraseCommand(str(entry["lba"]), str(entry["data"]))
            else:
                ValueError("wrong command in buffer")

        # erase buffer.txt
        with open("output/buffer.txt", 'w') as file:
            file.write('')


    def check_if_read_available(self, lba: int):

        for buffer_cmd in self.__buffer[::-1]:
            addr, value = self.__get_addr_and_value(buffer_cmd)
            if lba in addr:
                return value

        return None

    def __get_addr_and_value(self, buffer_cmd: dict):
        if buffer_cmd['cmd'] == 'W':
            return [buffer_cmd['lba']], buffer_cmd['data']
        elif buffer_cmd['cmd'] == 'E':
            start_addr = buffer_cmd['lba']
            end_addr = buffer_cmd['lba'] + int(buffer_cmd['data'])

            return list(range(start_addr, end_addr)), '0x00000000'
