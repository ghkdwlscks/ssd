import os


class Console:
    def __init__(self):
        dir_path = os.path.dirname(__file__)
        self.file_path = os.path.join(dir_path, "output", "result.txt")
        print(self.file_path)

    def is_exist_result_file(self):
        return os.path.exists(self.file_path)

    def read_result_file(self):
        data = ""
        try:
            with open(self.file_path, 'r') as file:
                data = file.read()
                data = data.strip()
        except:
            pass
        return data

    def read(self):
        if not self.is_exist_result_file():
            return False

        data = self.read_result_file()
        if len(data) == 0:
            return False

        print(data)
        return True
