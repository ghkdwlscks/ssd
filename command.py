import subprocess
import sys
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError


class ReadCommand(Command):
    def run(self):
        print("ReadCommand.run()")
        subprocess.run(["python", "ssd.py", "R", "0", "0x0"])


class ExitCommand(Command):
    def run(self):
        print("ExitCommand.run()")
        sys.exit()


class WriteCommand(Command):
    def __init__(self, index: int, value: str):
        self.__index = index
        self.__value = value

    def run(self):
        subprocess.run(["python", "ssd.py", "W", self.__index, self.__value])


class FullWriteCommand(Command):

    def __init__(self, value: str):
        self.__value = value

    def run(self):
        for index in range(100):
            write_command = WriteCommand(index, self.__value)
            write_command.run()


class HelpCommand(Command):

    def run(self):
        print("""
        - write: lba에 데이터를 기록합니다.
            write {{lba}} {{data}}
            
        - read: lba에 작성한 데이터를 읽습니다.
            read {{lba}}
            
        - exit: Shell을 종료합니다.
        
        - help: 도움말을 표시합니다.
        
        - fullwrite: 모든 lba에 해당 데이터를 기록합니다.
            fullwrite {{data}}
            
        - fullread: 모든 lba 데이터를 읽어 화면에 표시 합니다.
        """)
