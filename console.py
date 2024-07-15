import os


class Console:
    def __init__(self):
        self.file_path = os.path.join(os.getcwd(), "result.txt")

    def is_exist_result_file(self):
        return True if os.path.exists(self.file_path) else False

    def is_valid_index(self, idx: int):
        return True if (0 <= idx <= 99) else False

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
            print("[CONSOLE] NO RESULT.TXT")
            return False
        elif not self.is_valid_index(idx):
            print("[CONSOLE] INVALID LBA INDEX")
            return False
        else:
            data = self.read_result_file()

        if len(data) != 100:
            print("[CONSOLE] INVALID RESULT.TXT")
            return False

        sorted_data = sorted(data, key=lambda x: x[0])
        print(sorted_data[idx][1])
        return True
