from command import Command


class CommandFactory:
    def create_command(self, command):
        pass


class ShellCommandFactory(CommandFactory):
    def create_command(self, command: str):
        command = command.split()
        command_type = command[0]
        data1 = command[1] if len(command) >= 2 else None
        data2 = command[2] if len(command) >= 3 else None
        for sub_command in Command.__subclasses__():
            if sub_command.get_command_type() == command_type:
                return sub_command(data1, data2)


class SSDCommandFactory(CommandFactory):
    pass
