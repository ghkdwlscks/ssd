import os
import re
import sys

from console import Console
from constant import *


def can_convert_into_int(_target):
    try:
        int(_target)
    except ValueError:
        return False
    return True


def is_valid_lba(_lda):
    if can_convert_into_int(_lda) and int(_lda) < NUM_LBA:
        return True
    else:
        return False


def is_valid_data(_data):
    if re.fullmatch(r"0x[0-9A-F]{8}", _data):
        return True
    else:
        return False


class SSD:
    def __init__(self):
        self.cmd = ''
        self.lba = 0
        self.data = ''
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)
        self.nand_file_path = os.path.join(script_directory, os.getenv('NAND_TXT_PATH', 'output/nand.txt'))
        self.console = Console()

    def refresh_nand(self):
        with open(self.nand_file_path, 'w') as f:
            for i in range(NUM_LBA):
                f.write(f'{i} {VALUE_DEFAULT}\n')

    def set_command(self, cmd: str, lba: int, data: None or str = None):
        if cmd not in CMD_LIST:
            raise AttributeError
        if lba >= NUM_LBA:
            raise AttributeError
        self.cmd = cmd
        self.lba = lba
        self.data = data

    def run(self):
        if self.cmd == CMD_R:
            self.read()
        elif self.cmd == CMD_W:
            self.write()
        elif self.cmd == CMD_E:
            self.erase()

    def erase(self):
        '''
            시작 주소부터 size 크기만큼 default값으로 초기화합니다.
            마지막 주소를 넘어가면, 마지막 주소까지만 erase를 진행합니다.
        '''
        nand_read_result = self.__get_data_list_of_nand_file()

        for _lba in range(int(self.lba), int(self.lba) + int(self.data)):
            if _lba >= NUM_LBA:
                break
            nand_read_result[_lba] = [_lba, VALUE_DEFAULT]

        with open(self.nand_file_path, 'w') as f:
            f.writelines([f'{_lba} {_data}\n' for _lba, _data in nand_read_result])

    def read(self):
        nand_data_list = [x[1] for x in self.__get_data_list_of_nand_file()]
        self.console.write(nand_data_list[self.lba])

    def __read_nand(self):
        '''
        nand.txt를 읽어, list[[lba,data]]을 반환합니다.
        '''
        result = []
        try:
            with open(self.nand_file_path, 'r') as f:
                line = f.readline()

                while line:
                    lba, data = line.strip().split()
                    result.append([lba, data])
                    line = f.readline()
        except FileNotFoundError:
            self.refresh_nand()
            result = self.__read_nand()
        return result

    def __get_data_list_of_nand_file(self) -> list[list]:
        result = self.__read_nand()

        # validation check 에러시, nand 초기화 후 read  재 진행.
        if not self.__check_nand_validation(result):
            self.refresh_nand()
            result = self.__get_data_list_of_nand_file()

        return result

    def __check_nand_validation(self, nand_read_result):
        if len(nand_read_result) != NUM_LBA:
            return False
        for _lba, _data in nand_read_result:
            if is_valid_lba(_lba) and is_valid_data(_data):
                continue
            else:
                return False
        return True

    def write(self):
        '''
        nand.txt에  {lba} {data} 형식으로 write합니다.
        ex)
        0 0x0105AB55
        1 0x020202AA
        ....
        99 0x0404012
        '''
        nand_read_result = self.__get_data_list_of_nand_file()

        nand_read_result[self.lba] = [self.lba, self.data]

        with open(self.nand_file_path, 'w') as f:
            f.writelines([f'{_lba} {_data}\n' for _lba, _data in nand_read_result])


if __name__ == "__main__":
    args = sys.argv
    cmd = None
    lba = None
    data = None
    if len(args) >= 1:
        _ = args[0]
    if len(args) >= 2:
        cmd = args[1]
    if len(args) >= 3:
        lba = args[2]
    if len(args) >= 4:
        data = args[3]

    if is_valid_lba(lba):
        try:
            ssd = SSD()
            ssd.set_command(cmd, int(lba), data)
            ssd.run()
        except:
            print('SSD Error')
