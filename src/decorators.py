from src.logging_config import logger
import time

def log_method(func):
    """
    Decorator that logs the entry and exit of a method.
    """
    def wrapper(*args, **kwargs):
        logger.debug("Entering {}".format(func.__name__))
        logger.debug("Arguments: {}, {}".format(args, kwargs))
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.debug("Exiting {}".format(func.__name__))
        logger.debug("Return value: {}".format(result))
        logger.debug("Time elapsed: {}".format(end - start))
        return result
    return wrapper
