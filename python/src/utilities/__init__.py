import sys

from .buffer import Buffer
from .dot_dict import DotDict
from .event import Event
from .logging import *
from .math_utilities import *


def eprint(*args):
    print(*args, file=sys.stderr)
