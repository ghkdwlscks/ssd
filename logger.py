import functools
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
import logging


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    LOG_DIR = './/log'

    def __init__(self):
        self.logger = logging.getLogger('SingletonLogger')
        self.logger.setLevel(logging.DEBUG)
        log_format = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%y.%m.%d %H:%M')

        log_path = os.path.join(self.LOG_DIR, 'latest.log')
        self.handler = RotatingFileHandler(log_path, maxBytes=10240, backupCount=1, encoding='utf-8')  # 10kb 제한
        self.handler.setFormatter(log_format)
        self.logger.handlers = []
        self.logger.addHandler(self.handler)

        self.compress_old_logs()

    def log(self, instance, func_name, message):
        func_name_padded = f"{instance.__class__.__name__}.{func_name}()".ljust(50)
        self.logger.info(f'{func_name_padded}: {message}')
        self.rotate_log_files()

    def rotate_log_files(self):
        log_path = os.path.join(self.LOG_DIR, 'latest.log')
        if os.path.exists(log_path + '.1'):
            timestamp = datetime.now().strftime('%y%m%d_%H%M%S')
            os.rename(log_path + '.1', os.path.join(self.LOG_DIR, f'until_{timestamp}.log'))
            self.compress_old_logs()

    def compress_old_logs(self):
        logs = [f for f in os.listdir(self.LOG_DIR) if f.startswith('until_') and f.endswith('.log')]
        if len(logs) > 1:
            logs.sort()
            oldest_log = logs[0]
            oldest_log = os.path.join(self.LOG_DIR, oldest_log)
            os.rename(oldest_log, oldest_log.replace('.log', '.zip'))