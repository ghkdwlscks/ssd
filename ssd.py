import os
import sys

from constant import *
from ssd_command import SSDCommand


class SSD:
    def __init__(self):
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)
        self.nand_file_path = os.path.join(script_directory, os.getenv('NAND_TXT_PATH', 'output/nand.txt'))
        self.cmd = None

    def set_command(self, cmd: str, data1: str, data2: None or str = None):
        if cmd not in CMD_LIST:
            raise AttributeError('명령어의 Command 부분이 잘못되었습니다.')

        for ssd_command in SSDCommand.__subclasses__():
            if ssd_command.get_cmd_initial() == cmd:
                self.cmd = ssd_command(self, data1=data1, data2=data2)

    def run(self):
        if not self.cmd:
            raise ValueError('Command가 제대로 입력되지 않았습니다.')
        self.cmd.run()

    def refresh_nand(self):
        with open(self.nand_file_path, 'w') as f:
            for i in range(NUM_LBA):
                f.write(f'{i} {VALUE_DEFAULT}\n')


if __name__ == "__main__":
    args = sys.argv
    cmd = None
    data1 = None
    data2 = None
    if len(args) >= 1:
        _ = args[0]
    if len(args) >= 2:
        cmd = args[1]
    if len(args) >= 3:
        data1 = args[2]
    if len(args) >= 4:
        data2 = args[3]

    try:
        ssd = SSD()
        ssd.set_command(cmd, data1, data2)
        ssd.run()
    except Exception as error:
        print(error)
