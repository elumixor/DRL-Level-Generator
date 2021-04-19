from datetime import datetime
from typing import Union

import numpy as np
import torch

from .dot_dict import DotDict, to_dot_dict
from .memory_buffer import MemoryBuffer
from .printing import log
from .yaml_reading import read_yaml

num = Union[int, float]
vec = Union[np.ndarray, torch.tensor]


def clamp(value, _min, _max):
    return max(_min, min(value, _max))


def running_average(arr, smoothing=0.8):
    size = len(arr)
    res = np.zeros(size)

    if size == 0:
        return res

    res[0] = arr[0]
    for i in range(1, size):
        res[i] = res[i - 1] * smoothing + arr[i] * (1 - smoothing)

    return res


def approx(a: float, b: float, eps=1e-7):
    return abs(a - b) < eps


class timed:
    def __init__(self):
        self.start_time: float

    def __enter__(self):
        self.start_time = datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = datetime.now()
        total = end_time - self.start_time
        print(total)


# noinspection PyPep8Naming
class classproperty(property):
    # noinspection PyMethodOverriding
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()
