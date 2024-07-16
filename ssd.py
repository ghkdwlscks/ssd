import os
import re
import sys

from console import Console

CMD_LIST = ['R', 'W']


def can_convert_into_int(_target):
    try:
        int(_target)
    except ValueError:
        return False
    return True


def is_valid_lba(_lda):
    if can_convert_into_int(_lda) and int(_lda) < 100:
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
            for i in range(0, 100):
                f.write(f'{i} 0x00000000\n')

    def set_command(self, cmd: str, lba: int, data: None or str = None):
        if cmd not in CMD_LIST:
            raise AttributeError
        if lba >= 100:
            raise AttributeError
        self.cmd = cmd
        self.lba = lba
        self.data = data

    def run(self):
        if self.cmd == 'R':
            self.read()
        elif self.cmd == 'W':
            self.write()

    def read(self):
        nand_data_list = [x[1] for x in self.__get_data_list_of_nand_file()]
        self.console.write(nand_data_list[self.lba])

    '''
    nand.txt를 읽어, list[[lba,data]]을 반환합니다.
    '''
    def __read_nand(self):
        result = []
        try:
            with open(self.nand_file_path, 'r') as f:
                line = f.readline()

                while line:
                    lba, data = line.strip().split()
                    result.append([lba, data])
                    line = f.readline()
        except:
            self.refresh_nand()
            result = self.__read_nand()
        return result

    # validation check 에러시, nand 초기화 후 read 진행.
    def __get_data_list_of_nand_file(self) -> list[list[int, str]]:
        result = self.__read_nand()

        if not self.__check_nand_validation(result):
            self.refresh_nand()
            self.__get_data_list_of_nand_file()

        return result

    def __check_nand_validation(self, read_result):
        # nand 데이터 유효성 검사
        if len(read_result) != 100:
            raise ValueError
        for _lba, _data in read_result:
            if is_valid_lba(_lba) and is_valid_data(_data):
                continue
            else:
                return False
        return True

    '''
    nand.txt에 write되는 형식
    {lba} {data}
    
    ex)
    0 0x0105AB55
    1 0x020202AA
    ....
    99 0x0404012
    '''

    def write(self):
        lines = self.__read_nand()

        new_line_content = [self.lba, self.data]
        lines[self.lba] = new_line_content

        with open(self.nand_file_path, 'w') as f:
            f.writelines([f'{_lba} {_data}\n' for _lba, _data in lines])


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

    ssd = SSD()
    ssd.set_command(cmd, int(lba), data)
    ssd.run()
