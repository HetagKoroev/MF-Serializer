"""Логирование с записью в файл logfile.log"""


from datetime import datetime
from typing import Callable


def log_it(func: Callable):
    """Декоратор логирования"""
    def wrapper(*args, **kwargs):
        f_name: str = str(func).split()[1]
        start_time = datetime.now()
        try:
            result = func(*args, **kwargs)
            msg: str = f'Функция <{f_name}> запущена в "{start_time}" - и успешно' \
                       f' завершена.", \n\n'
            with open('logfile.log', 'a+') as file:
                file.write(msg)
            return result
        except RuntimeError as err:
            msg: str = f'Функция <{f_name}> запущена в "{start_time}" - и завершена с' \
                       f' "{err}" - ошибкой."\n\n'
            with open('logfile.log', 'a+') as file:
                file.write(msg)
    return wrapper
