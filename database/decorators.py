import logging
from functools import wraps

from mongoengine.errors import NotUniqueError


logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s -%(levelname)s -%(message)s",
)


def error_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            logging.error(f"Exception '{func.__name__}': => {err}")
        except ValueError as err:
            logging.error(f"ValueError' {func.__name__}': => {err}")
        except KeyError as err:
            logging.error(f"KeyError' {func.__name__}': => {err}")
        except NotUniqueError as err:
            logging.error(f"NotUniqueError' {func.__name__}': => {err}")
        return None

    return wrapper
