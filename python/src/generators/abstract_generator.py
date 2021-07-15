import abc

import torch
from torch import Tensor


class AbstractGenerator(abc.ABC):
    def __init__(self, bounds: Tensor):
        if bounds.ndim != 2 or bounds.shape[-1] != 2:
            raise Exception(f"'bounds' should have shape (dimension_count, 2), but was {bounds.shape}")

        self.bounds = bounds
        self.embedding_size = bounds.shape[0]

        self.bounds_min = bounds[:, 0]
        self.bounds_max = bounds[:, 1]

        self.bounds_diff = self.bounds_max - self.bounds_min

        if not torch.all(self.bounds_min <= self.bounds_max):
            raise Exception("minimum values of the 'bounds' should be smaller than the maximums")

    @abc.abstractmethod
    def generate(self, d_in):
        pass

    def __call__(self, *args, **kwargs):
        self.generate(*args, **kwargs)

    def remap(self, x):
        return x * self.bounds_diff + self.bounds_min

    def remap_inverse(self, x):
        return (x - self.bounds_min) / self.bounds_diff
