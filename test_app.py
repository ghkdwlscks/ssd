from command import make_command


class TestApp:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.commands = self.__read_script_file()

    def __read_script_file(self) -> list[str]:
        with open(self.filename) as file:
            return [line.strip() for line in file]

    def run(self):
        for command in self.commands:
            self.__run_command(command)
        if self.__validate():
            print(f"{self.__class__.__name__} passed")
        else:
            print(f"{self.__class__.__name__} failed")

    @staticmethod
    def __run_command(command: str) -> None:
        command = make_command(command.strip())
        command.run()

    def __validate(self) -> bool:
        pass


class TestApp1(TestApp):

    def __validate(self) -> bool:
        pass


class TestApp2(TestApp):

    def __validate(self) -> bool:
        pass


def make_test_app(command: str) -> TestApp:
    if command == "testapp1":
        return TestApp1("script/test_app1.txt")
    elif command == "testapp2":
        return TestApp2("script/test_app2.txt")
