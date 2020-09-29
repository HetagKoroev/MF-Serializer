from datetime import datetime
from typing import Callable


def log_it(f: Callable):
    def wrapper(*args, **kwargs):
        f_name: str = str(f).split()[1]
        start_time = datetime.now()
        try:
            result = f(*args, **kwargs)
            msg: str = f'Функция <{f_name}> запущена в "{start_time}" - и успешно завершена.", \n\n'
            with open('logfile.log', 'a+') as fl:
                fl.write(msg)
            return result
        except Exception as err:
            msg: str = f'Функция <{f_name}> запущена в "{start_time}" - и завершена с "{err}" - ошибкой."\n\n'
            with open('logfile.log', 'a+') as fl:
                fl.write(msg)
    return wrapper
