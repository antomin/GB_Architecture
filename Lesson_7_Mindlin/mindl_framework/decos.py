from functools import wraps
from time import time


def debug(obj):
    @wraps(obj)
    def wrapper(*args, **kwargs):
        start_time = time()
        result = obj(*args, **kwargs)
        print(f'Контроллер {obj.__name__} выполнен за {round(time() - start_time, 4)}сек.')
        return result
    return wrapper
