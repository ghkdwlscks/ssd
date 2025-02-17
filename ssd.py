import os
import sys

from buffer import Buffer
from command_factory import SSDCommandFactory
from constant import *


class SSD:
    def __init__(self):
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)
        self.nand_file_path = os.path.join(script_directory, os.getenv('NAND_TXT_PATH', 'output/nand.txt'))
        self.cmd = None
        self.buffer = Buffer()

    def set_command(self, command: str):
        cmd_type = command.split()[0]
        if cmd_type not in CMD_LIST:
            raise AttributeError('명령어의 Command 부분이 잘못되었습니다.')

        self.cmd = SSDCommandFactory(command).create_command()

    def run(self):
        if not self.cmd:
            raise ValueError('Command가 제대로 입력되지 않았습니다.')
        try:
            if self.cmd.get_command_type() == CMD_R:
                if not self.buffer.read_from_buffer_if_available(self.cmd.lba):
                    self.cmd.run()
            elif self.cmd.get_command_type() == CMD_W:
                self.buffer.add(self.cmd.get_command_type(), self.cmd.lba, self.cmd.data)
            elif self.cmd.get_command_type() == CMD_E:
                self.buffer.add(self.cmd.get_command_type(), self.cmd.lba, self.cmd.size)
            elif self.cmd.get_command_type() == CMD_F:
                self.buffer.flush()
        except Exception as e:
            print(e)
            print('에러 Fix를 위해 nand를 초기화합니다.')
            self.refresh_nand()
            self.run()
            print('예약된 동작을 재시작합니다.')

    def refresh_nand(self):
        with open(self.nand_file_path, 'w') as f:
            for i in range(NUM_LBA):
                f.write(f'{i} {VALUE_DEFAULT}\n')
        self.buffer.refresh_buffer()


if __name__ == "__main__":
    try:
        ssd = SSD()
        ssd.set_command(' '.join(sys.argv[1:]))
        ssd.run()
    except Exception as error:
        print(error)
