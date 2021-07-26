import os
from datetime import datetime
from typing import Union

import torch
from torch import Tensor

from .dot_dict import DotDict, to_dot_dict
from .epsilon_decay import EpsilonDecay
from .math_utils import *
from .memory_buffer import MemoryBuffer
from .mlp import MLP
from .printing import log
from .sci_utils import *
from .setter import setter
from .train_until import TrainUntil
from .yaml_reading import read_yaml

num = Union[int, float]
vec = Union[np.ndarray, torch.tensor]


def save(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if issubclass(type(obj), torch.nn.Module):
        torch.save(obj, path)
        return

    torch.save(obj, path)


def load(path, none_on_error=False):
    try:
        return torch.load(path)
    except FileNotFoundError as e:
        if none_on_error:
            return None
        raise e


def discounted_rewards(rewards: Tensor, discounting: float):
    res = torch.zeros_like(rewards)
    last = torch.zeros_like(rewards[0])

    for i in reversed(range(rewards.shape[0])):
        last = res[i] = rewards[i] + discounting * last

    return res


def set_matplotlib_colors(matplotlib, text_color="black", other_color="white", label_color="white"):
    matplotlib.rcParams["axes.labelcolor"] = label_color

    for p in ['xtick.color', 'ytick.color']:
        matplotlib.rcParams[p] = other_color

    matplotlib.rcParams['text.color'] = text_color


def sample_from(dataset: Tensor, size: int, indices=False):
    i = torch.randperm(dataset.shape[0])[:size]

    if not indices:
        return dataset[i]
    else:
        return dataset[i], i


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
