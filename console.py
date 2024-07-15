import os


class Console:
    def __init__(self):
        self.file_path = os.path.join(os.getcwd(), "result.txt")

    def is_exist_result_file(self):
        return os.path.exists(self.file_path)

    def is_valid_index(self, idx: int):
        return 0 <= idx <= 99

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

    def read(self, idx: int):
        if not self.is_exist_result_file():
            return False
        elif not self.is_valid_index(idx):
            return False
        else:
            data = self.read_result_file()

        return self.find_and_print_value_if_exist(data, idx)

    def find_and_print_value_if_exist(self, data, idx):
        for row in data:
            if row[0] == idx:
                print(row[1])
                return True
        return False
