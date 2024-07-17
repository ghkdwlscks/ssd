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
        # Flush When Buffer is Full
        if len(self.__buffer) >= 10:
            self.flush()

        entry = {"cmd": cmd, "lba": int(lba), "data": data}
        if cmd == "E":
            data = int(data)
        self.__buffer.append(entry)

        # Optimize
        self.optimize_unnecessary_commands()

        # TODO: Call optimize functions
        with open("output/buffer.txt", "w") as file:
            for entry in self.__buffer:
                file.write(f"{entry['cmd']} {entry['lba']} {entry['data']}\n")

    def flush(self) -> None:
        for entry in self.__buffer:
            if entry['cmd'] == CMD_W:
                WriteCommand(str(entry["lba"]), entry["data"])
            elif entry['cmd'] == CMD_E:
                EraseCommand(str(entry["lba"]), str(entry["data"]))
            else:
                ValueError("wrong command in buffer")

        # erase buffer.txt
        self.__buffer = list()
        with open("output/buffer.txt", 'w') as file:
            file.write('')

    def optimize_merge_sequence_erase(self):
        before, after = self.__buffer[-2], self.__buffer[-1]

        if before['cmd'] != CMD_E or after['cmd'] != CMD_E:
            return

        before_arr = set(range(before['lba'], before['lba'] + before['data']))
        after_arr = set(range(after['lba'], after['lba'] + after['data']))
        new_arr = list(before_arr | after_arr)
        sorted_arr = sorted(new_arr)

        if self.is_consecutive(new_arr):
            self.__buffer.pop(-1)
            self.__buffer.pop(-1)
            self.add('E', sorted_arr[0], len(sorted_arr))

    def optimize_narrow_range_of_erase(self):

        for erase in self.__buffer:
            if erase['cmd'] != CMD_E: continue

            erase_arr = list(range(erase['lba'], erase['lba'] + erase['data']))

            for write in self.__buffer:
                if write['cmd'] != CMD_W: continue

                erase_arr.remove(write['lba'])

            # if self.is_consecutive(erase_arr):












    def is_consecutive(self, arr):
        sorted_arr = sorted(arr)
        for i in range(1, len(sorted_arr)):
            if sorted_arr[i] != sorted_arr[i-1] +1:
                return False
        return True


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

    def optimize_unnecessary_commands(self):
        addr_list = []
        for buffer_cmd in self.__buffer:
            addr, _ = self.__get_addr_and_value(buffer_cmd)
            addr_list.append(addr)

        drop_ids = []
        buffer_len = len(self.__buffer)
        for i in range(buffer_len):
            for j in range(i + 1, buffer_len):
                if set(addr_list[i]).issubset(addr_list[j]):
                    drop_ids.append(i)
                    break
        self.__buffer = [element for i, element in enumerate(self.__buffer) if i not in drop_ids]
