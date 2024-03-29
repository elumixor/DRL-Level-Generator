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
        """
        Generates levels of the given difficulties in embedding space
        :param d_in: Difficulty, that the generated level should have
        :return: Generated level
        """
        pass

    def __call__(self, *args, **kwargs):
        return self.generate(*args, **kwargs)

    def to_embedding(self, x):
        """
        Maps [0, 1] to the embeddings space
        """
        return x * self.bounds_diff + self.bounds_min

    def from_embedding(self, x):
        """
        Maps embedding space back to the [0, 1] range
        """
        return (x - self.bounds_min) / self.bounds_diff
