import os


class Console:
    def __init__(self):
        dir_path = os.path.dirname(__file__)
        self.file_path = os.path.join(dir_path, "output", "result.txt")

    def is_exist_result_file(self):
        return os.path.exists(self.file_path)

    def read_result_file(self):
        try:
            with open(self.file_path, 'r') as file:
                data = file.read().strip()
        except FileNotFoundError:
            data = ""
        return data

    def read(self):
        if not self.is_exist_result_file():
            return
        if not (result := self.read_result_file()):
            return
        print(result)

    def write(self, data):
        if not self.is_exist_result_file():
            return

        with open(self.file_path, "w") as result_file:
            result_file.write(data)
