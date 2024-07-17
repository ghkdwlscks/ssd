import functools
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
import logging


class CustomLogger:
    def __init__(self):
        self.logger = logging.getLogger('SingletonLogger')
        self.logger.setLevel(logging.DEBUG)
        log_format = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%y.%m.%d %H:%M')

        self.handler = RotatingFileHandler('latest.log', maxBytes=10240, backupCount=1)  # 10kb 제한
        self.handler.setFormatter(log_format)
        self.logger.handlers = []  # 기존 핸들러 제거
        self.logger.addHandler(self.handler)

        self.compress_old_logs()

    def log(self, func_name, message):
        func_name_padded = f"{func_name}()".ljust(30)
        self.logger.info(f'{func_name_padded}: {message}')
        self.rotate_log_files()

    def rotate_log_files(self):
        if os.path.exists('latest.log.1'):
            timestamp = datetime.now().strftime('%y%m%d_%H%M%S')
            os.rename('latest.log.1', f'until_{timestamp}.log')
            self.compress_old_logs()

    def compress_old_logs(self):
        logs = [f for f in os.listdir('.') if f.startswith('until_') and f.endswith('.log')]
        if len(logs) > 1:
            logs.sort()
            oldest_log = logs[0]
            os.rename(oldest_log, oldest_log.replace('.log', '.zip'))

    @classmethod
    def custom_logger(cls, message):
        def decorator(func):
            @functools.wraps(func)
            def wrapper_logger(*args, **kwargs):
                func_name = func.__name__
                cls().log(func_name, f'{message} - 호출됨: args={args}, kwargs={kwargs}')
                result = func(*args, **kwargs)
                cls().log(func_name, f'{message} - 반환값: {result}')
                return result

            return wrapper_logger

        return decorator
