import io
import sys

from command import make_command


class TestApp:
    def __init__(self, test_name: str) -> None:
        self.test_name = test_name
        self.file_name = f"script/{test_name}.txt"
        self.commands, self.answer = self.__read_script_file()
        self.output = None

    def __parse_command_answer_file(self, lines: list[str]):
        commands = []
        answer = []

        command_flag = 0
        answer_flag = 0

        for line in lines:
            if line.startswith('#') and 'command' in line.lower():
                command_flag = 1
                answer_flag = 0
            elif line.startswith('#') and 'answer' in line.lower():
                command_flag = 0
                answer_flag = 1
            elif command_flag == 1:
                commands.append(line)
            elif answer_flag == 1:
                answer.append(line)

        return commands, '\n'.join(answer)

    def __read_script_file(self):
        with open(self.file_name, 'r') as file:
            lines = [line.strip() for line in file]
        return self.__parse_command_answer_file(lines)

    def run(self):
        print(f"{self.test_name} --- Run...", end='')

        old_stdout = sys.stdout
        self.output = io.StringIO()
        sys.stdout = self.output

        for command in self.commands:
            self._run_command(command)

        is_valid = self._validate()
        sys.stdout = old_stdout
        if is_valid:
            print(f"Pass")
            return True
        else:
            print(f"FAIL!")
            return False

    @staticmethod
    def _run_command(command: str) -> None:
        command = make_command(command.strip())
        command.run()

    def _validate(self) -> bool:
        return self.output.getvalue().strip() == self.answer.strip()
