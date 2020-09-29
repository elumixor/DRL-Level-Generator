import torch

from utilities.event import *
from utilities.byte_conversions import *
from utilities.logging import *


def bootstrap(rewards, last, discounting=0.99):
    res = torch.zeros_like(rewards)
    for i in reversed(range(rewards.shape[0])):
        last = res[i] = rewards[i] + discounting * last
    return res


def normalize(tensor):
    return (tensor - tensor.mean()) / tensor.std()
