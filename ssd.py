import os
import sys

RESULT_FILE = '../output/result.txt'
NAND_FILE = '../output/nand.txt'

CMD_LIST = ['R', 'W', 'FR']


class SSD:
    def __init__(self):
        self.cmd = ''
        self.lba = 0
        self.data = ''
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)
        self.result_file_path = os.path.join(script_directory, os.getenv('RESULT_TXT_PATH', 'output/result.txt'))
        self.nand_file_path = os.path.join(script_directory, os.getenv('NAND_TXT_PATH', 'output/nand.txt'))

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
        elif self.cmd == 'FR':
            self.full_read()

    def full_read(self):

        try:
            nand_data_list = self.__get_data_list_of_nand_file()
        except:
            self.refresh_nand()
            nand_data_list = self.__get_data_list_of_nand_file()

        with open(self.result_file_path, 'w') as f:
            f.write('\n'.join(nand_data_list))

    def read(self):
        try:
            nand_data_list = self.__get_data_list_of_nand_file()
        except:
            self.refresh_nand()
            nand_data_list = self.__get_data_list_of_nand_file()

        with open(self.result_file_path, 'w') as f:
            f.write(nand_data_list[self.lba])

    def __get_data_list_of_nand_file(self):
        result = []
        with open(self.nand_file_path, 'r') as f:
            line = f.readline()
            while line:
                lba, data = line.split()
                result.append(data)
                line = f.readline()
        return result

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
        try:
            with open(self.nand_file_path, 'r') as f:
                lines = f.readlines()
        except:
            self.refresh_nand()
            with open(self.nand_file_path, 'r') as f:
                lines = f.readlines()

        if self.lba >= len(lines):
            raise SystemError

        new_line_content = f'{self.lba} {self.data}\n'
        lines[self.lba] = new_line_content

        with open(self.nand_file_path, 'w') as f:
            f.writelines(lines)


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
