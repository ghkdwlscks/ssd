import os


class Console:
    def __init__(self):
        dir_path = os.path.dirname(__file__)
        self.file_path = os.path.join(dir_path, "output", "result.txt")

    def is_exist_result_file(self):
        return os.path.exists(self.file_path)

    def read_result_file(self):
        results = []
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    index, value = line.split()
                    results.append((int(index), value))
        except:
            pass
        return results

    def print_result_file(self, result_file):
        for data in result_file:
            print(data[1])

    def read(self):
        if not self.is_exist_result_file():
            return False

        data = self.read_result_file()
        if len(data) == 0:
            return False

        self.print_result_file(data)
        return True
