from typing import Union

from .byte_reader import ByteReader
from .clamp import Clamp
from .decorators import *
from .is_greater import IsGreater, is_greater
from .lru_list import LRUList
from .memory_buffer import MemoryBuffer
from .mlp import mlp as MLP
from .printing import log, style, set_style, get_styles
from .remap import Remap

num = Union[float, int]
