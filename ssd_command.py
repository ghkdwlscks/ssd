import os
from abc import ABC

from command import Command
from console import Console
from constant import NUM_LBA, VALUE_DEFAULT, CMD_R, CMD_W, CMD_E, CMD_F
from utils import check_nand_txt_read_result_validation, is_valid_lba, is_valid_data, can_convert_into_int


class SSDCommand(Command, ABC):

    def __init__(self, data1, data2):
        super().__init__(data1, data2)
        self.console = Console()
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)
        self.nand_file_path = os.path.join(script_directory, os.getenv('NAND_TXT_PATH', 'output/nand.txt'))

    def _read_nand(self):
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
            raise FileNotFoundError('nand.txt가 경로에 없습니다.')
        return result

    def _get_data_list_of_nand_file(self) -> list[list]:
        result = self._read_nand()

        # validation check 에러시, nand 초기화 후 read  재 진행.
        if not check_nand_txt_read_result_validation(result):
            raise ValueError('nand.txt의 데이터에 오류가 있습니다.')

        return result


class SSDReadCommand(SSDCommand):
    @staticmethod
    def get_command_type():
        return CMD_R

    def __init__(self, data1, data2):
        super().__init__(data1, data2)
        if is_valid_lba(data1):
            self.lba = int(data1)
        else:
            raise AttributeError('Read할 Address가 유효하지 않습니다.')

    def run(self):
        nand_data_list = [x[1] for x in self._get_data_list_of_nand_file()]
        self.console.write(nand_data_list[self.lba])


class SSDWriteCommand(SSDCommand):
    @staticmethod
    def get_command_type():
        return CMD_W

    def __init__(self, data1, data2):
        super().__init__(data1, data2)
        if is_valid_lba(data1):
            self.lba = int(data1)
        else:
            raise ValueError('Write할 Address가 유효하지 않습니다.')

        if is_valid_data(data2):
            self.data = data2
        else:
            raise ValueError('Write할 데이터가 유효하지 않습니다.')

    def run(self):
        """
                nand.txt에  {lba} {data} 형식으로 write합니다.
                ex)
                0 0x0105AB55
                1 0x020202AA
                ....
                99 0x0404012
                """
        nand_read_result = self._get_data_list_of_nand_file()

        nand_read_result[self.lba] = [self.lba, self.data]

        with open(self.nand_file_path, 'w') as f:
            f.writelines([f'{_lba} {_data}\n' for _lba, _data in nand_read_result])


class SSDEraseCommand(SSDCommand):
    @staticmethod
    def get_command_type():
        return CMD_E

    def __init__(self, data1, data2):
        super().__init__(data1, data2)
        if is_valid_lba(data1):
            self.lba = int(data1)
        else:
            raise ValueError('Erase할 Address가 유효하지 않습니다.')

        if can_convert_into_int(data2) and int(data2) <= NUM_LBA:
            self.size = data2
        else:
            raise ValueError('Erase할 사이즈가 유효하지 않습니다.')

    def run(self):
        '''
                    시작 주소부터 size 크기만큼 default값으로 초기화합니다.
                    마지막 주소를 넘어가면, 마지막 주소까지만 erase를 진행합니다.
                '''
        nand_read_result = self._get_data_list_of_nand_file()

        for _lba in range(int(self.lba), int(self.lba) + int(self.size)):
            if _lba >= NUM_LBA:
                break
            nand_read_result[_lba] = [_lba, VALUE_DEFAULT]

        with open(self.nand_file_path, 'w') as f:
            f.writelines([f'{_lba} {_data}\n' for _lba, _data in nand_read_result])


class SSDFlushCommand(SSDCommand):
    def __init__(self, data1, data2):
        super().__init__(data1, data2)

    @staticmethod
    def get_command_type():
        return CMD_F

    def run(self):
        pass
