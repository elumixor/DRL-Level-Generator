import functools
import sys
from datetime import timedelta

from .buffer import Buffer
from .event import Event
from .logging import *
from .math_utilities import *


def eprint(*args):
    print(*args, file=sys.stderr)


def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"{func.__name__}()")
        func(*args, **kwargs)

    return wrapper


def clamp(value, _min, _max):
    return max(_min, min(value, _max))


def time_string(seconds):
    return str(timedelta(seconds=round(seconds)))
