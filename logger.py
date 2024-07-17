import os
from datetime import datetime
import inspect


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    LOG_DIR = './/log'
    LOG_FILE = LOG_DIR + '//latest.log'
    MAX_SIZE = 10240
    ENCODING = 'utf-8'

    def __init__(self):
        self.make_log_file()

    def make_log_file(self):
        os.makedirs(self.LOG_DIR, exist_ok=True)

        if not os.path.exists(self.LOG_FILE):
            with open(self.LOG_FILE, "w", encoding=self.ENCODING):
                pass

    def log(self, message):
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__.__name__
        the_method = stack[1][0].f_code.co_name

        timestamp = datetime.now().strftime("%y.%m.%d %H:%M")
        formatted_function_name = ("[" + timestamp + "] " + the_class + "." + the_method + "()").ljust(70)
        log_message = f"{formatted_function_name}:{message}\n"
        self.logging(log_message)

    def logging(self, log_message):
        with open(self.LOG_FILE, "a", encoding=self.ENCODING) as logfile:
            logfile.write(log_message)
        self.rotate_log_files()

    def rotate_log_files(self):
        if os.path.getsize(self.LOG_FILE) > self.MAX_SIZE:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            rename_file_name = f"/until_{timestamp}.log"
            os.rename(self.LOG_FILE, self.LOG_DIR + rename_file_name)
        self.make_log_file()
        self.compress_old_logs()

    def compress_old_logs(self):
        logs = [f for f in os.listdir(self.LOG_DIR) if f.startswith('until_') and f.endswith('.log')]
        if len(logs) > 1:
            logs.sort()
            oldest_log = logs[0]
            oldest_log = os.path.join(self.LOG_DIR, oldest_log)
            os.rename(oldest_log, oldest_log.replace('.log', '.zip'))
