import io
import sys

from command import make_command


class TestApp:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.commands = self.__read_script_file()
        self.output = None

    def __read_script_file(self) -> list[str]:
        with open(self.filename) as file:
            return [line.strip() for line in file]

    def run(self):
        print(f"Running {self.__class__.__name__} ..")
        old_stdout = sys.stdout
        self.output = io.StringIO()
        sys.stdout = self.output
        for command in self.commands:
            self._run_command(command)
        is_valid = self._validate()
        sys.stdout = old_stdout
        if is_valid:
            print(f"{self.__class__.__name__} passed")
        else:
            print(f"{self.__class__.__name__} failed")

    @staticmethod
    def _run_command(command: str) -> None:
        command = make_command(command.strip())
        command.run()

    def _validate(self) -> bool:
        pass


class TestApp1(TestApp):

    def _validate(self) -> bool:
        self._run_command("fullread")
        return len(set(self.output.getvalue().splitlines())) == 1


class TestApp2(TestApp):

    def _validate(self) -> bool:
        pass


def make_test_app(command: str) -> TestApp:
    if command == "testapp1":
        return TestApp1("script/test_app1.txt")
    elif command == "testapp2":
        return TestApp2("script/test_app2.txt")
