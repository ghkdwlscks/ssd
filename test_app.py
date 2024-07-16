from abc import ABC, abstractmethod


class TestApp(ABC):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.commands = self.__read_script_file()

    def __read_script_file(self) -> list[str]:
        pass

    def run(self):
        for command in self.commands:
            output = self.__run_command(command)
            if not self.__validate_result(command, output):
                print(f"{self.__class__.__name__} failed")
                return
        print(f"{self.__class__.__name__} success")

    def __run_command(self, command: str) -> str:
        pass

    @abstractmethod
    def __validate_result(self, command: str, output: str) -> bool:
        raise NotImplementedError


class TestApp1(TestApp):

    def __validate_result(self, command: str, output: str) -> bool:
        pass


class TestApp2(TestApp):

    def __validate_result(self, command: str, output: str) -> bool:
        pass


def run_test_app(command: str) -> None:
    if command == "testapp1":
        TestApp1("test_app1.txt").run()
    elif command == "testapp2":
        TestApp2("test_app2.txt").run()
