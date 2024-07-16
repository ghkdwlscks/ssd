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
        self.result_file_path = os.path.join(script_directory, os.getenv('RESULT_TXT_PATH', '/output/result.txt'))
        self.nand_file_path = os.path.join(script_directory, os.getenv('NAND_TXT_PATH', '/output/nand.txt'))

    def refresh_nand(self):
        with open(self.nand_file_path, 'w') as f:
            for i in range(0, 100):
                f.write(f'{i} 0x00000000\n')

    def set_command(self, cmd, lba, data=None):
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
        result = []
        try:
            with open(self.nand_file_path, 'r') as f:
                line = f.readline()
                while line:
                    lba, data = line.split()
                    result.append(data)
                    line = f.readline()
        except:
            self.refresh_nand()

        with open(self.result_file_path, 'w') as f:
            f.write('\n'.join(result))

    def read(self):
        result = ''
        try:
            with open(self.nand_file_path, 'r') as f:
                line = f.readline()
                while line:
                    lba, data = line.split()
                    if int(lba) == self.lba:
                        result = data
                        break
                    line = f.readline()
        except:
            self.refresh_nand()

        with open(self.result_file_path, 'w') as f:
            f.write(result)
        print(f'{self.lba} read')

    def write(self):
        with open(self.nand_file_path, 'r') as file:
            lines = file.readlines()

        # 수정할 줄 선택
        if self.lba < len(lines):
            line_to_modify = lines[self.lba]

            new_line_content = f'{self.lba} {self.data}\n'
            lines[self.lba] = new_line_content

            # 파일을 쓰기 모드로 열어서 수정된 내용 쓰기
            with open(self.nand_file_path, 'w') as file:
                file.writelines(lines)


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

    SSD().set_command(cmd, int(lba), data)
    SSD().run()
