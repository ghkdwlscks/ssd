from abc import ABC, abstractmethod

from command import Command


class CommandFactory(ABC):

    @abstractmethod
    def create_command(self):
        pass


class ShellCommandFactory(CommandFactory):
    def __init__(self, command: str):
        command = command.split()
        self.command_type = command[0]
        self.data1 = command[1] if len(command) >= 2 else None
        self.data2 = command[2] if len(command) >= 3 else None

    def create_command(self):
        for sub_command in Command.__subclasses__():
            if sub_command.get_command_type() == self.command_type:
                return sub_command(self.data1, self.data2)


class SSDCommandFactory(CommandFactory):
    pass
