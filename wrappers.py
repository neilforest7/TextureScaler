from functools import wraps


def func_timer(orig_func):
    import time

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1
        print(f'Function:[{orig_func.__name__}] ran in ::::: {t2} seconds')
        return result

    return wrapper


def func_logger(orig_func):
    import logging
    logging.basicConfig(filename=f'{orig_func.__name__}.log', level=logging.INFO)

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        logging.info(f'Ran with args {args}, and kwargs {kwargs}')
        return orig_func(*args, **kwargs)

    return wrapper
