from abc import ABC, abstractmethod

from console import Console
from constant import NUM_LBA, VALUE_DEFAULT, CMD_R, CMD_W, CMD_E
from functions import check_nand_txt_read_result_validation, is_valid_lba, is_valid_data, can_convert_into_int


class SSDCommand(ABC):
    @staticmethod
    @abstractmethod
    def get_cmd_initial():
        pass

    @abstractmethod
    def run(self):
        pass

    def __init__(self, ssd, **kwargs):
        self.console = Console()
        self.ssd = ssd

    def _refresh_nand(self):
        with open(self.ssd.nand_file_path, 'w') as f:
            for i in range(NUM_LBA):
                f.write(f'{i} {VALUE_DEFAULT}\n')

    def _read_nand(self):
        '''
        nand.txt를 읽어, list[[lba,data]]을 반환합니다.
        '''
        result = []
        try:
            with open(self.ssd.nand_file_path, 'r') as f:
                line = f.readline()

                while line:
                    lba, data = line.strip().split()
                    result.append([lba, data])
                    line = f.readline()
        except FileNotFoundError:
            self._refresh_nand()
            result = self._read_nand()
        return result

    def _get_data_list_of_nand_file(self) -> list[list]:
        result = self._read_nand()

        # validation check 에러시, nand 초기화 후 read  재 진행.
        if not check_nand_txt_read_result_validation(result):
            self._refresh_nand()
            result = self._get_data_list_of_nand_file()

        return result


class SSDReadCommand(SSDCommand):
    @staticmethod
    def get_cmd_initial():
        return CMD_R

    def __init__(self, ssd, **kwargs):
        super().__init__(ssd, **kwargs)
        if is_valid_lba(kwargs['data1']):
            self.lba = int(kwargs['data1'])
        else:
            raise AttributeError('Read할 Address가 유효하지 않습니다.')

    def run(self):
        nand_data_list = [x[1] for x in self._get_data_list_of_nand_file()]
        self.console.write(nand_data_list[self.lba])


class SSDWriteCommand(SSDCommand):
    @staticmethod
    def get_cmd_initial():
        return CMD_W

    def __init__(self, ssd, **kwargs):
        super().__init__(ssd, **kwargs)
        if is_valid_lba(kwargs['data1']):
            self.lba = int(kwargs['data1'])
        else:
            raise ValueError('Write할 Address가 유효하지 않습니다.')

        if is_valid_data(kwargs['data2']):
            self.data = kwargs['data2']
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

        with open(self.ssd.nand_file_path, 'w') as f:
            f.writelines([f'{_lba} {_data}\n' for _lba, _data in nand_read_result])


class SSDEraseCommand(SSDCommand):
    @staticmethod
    def get_cmd_initial():
        return CMD_E

    def __init__(self, ssd, **kwargs):
        super().__init__(ssd, **kwargs)
        if is_valid_lba(kwargs['data1']):
            self.lba = int(kwargs['data1'])
        else:
            raise ValueError('Erase할 Address가 유효하지 않습니다.')

        if can_convert_into_int(kwargs['data2']) and int(kwargs['data2']) <= NUM_LBA:
            self.size = kwargs['data2']
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

        with open(self.ssd.nand_file_path, 'w') as f:
            f.writelines([f'{_lba} {_data}\n' for _lba, _data in nand_read_result])
