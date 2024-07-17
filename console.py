import os

from logger import Logger


class Console:
    def __init__(self):
        dir_path = os.path.dirname(__file__)
        self.file_path = os.path.join(dir_path, "output", "result.txt")
        self.logger = Logger()

    def is_exist_result_file(self):
        return os.path.exists(self.file_path)

    def read_result_file(self):
        try:
            self.logger.log(self, "read_result_file()", "result.txt read")
            with open(self.file_path, 'r') as file:
                data = file.read().strip()
        except FileNotFoundError:
            self.logger.log(self, "read_result_file()", "Fail - FileNotFoundError 발생")
            data = ""
        return data

    def read(self):
        self.logger.log(self, "read()", "console read")
        if not self.is_exist_result_file():
            return
        if not (result := self.read_result_file()):
            return
        print(result)

    def write(self, data):
        self.logger.log(self, "write()", "console write")
        if not self.is_exist_result_file():
            return

        with open(self.file_path, "w") as result_file:
            result_file.write(data)
