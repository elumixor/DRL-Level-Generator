import functools
import sys

from .buffer import Buffer
from .dot_dict import DotDict
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
