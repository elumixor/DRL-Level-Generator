from abc import ABC, abstractmethod

import numpy as np

from utils import vec


class Space(ABC):
    @property
    @abstractmethod
    def size(self) -> int: ...

    @abstractmethod
    def sample(self, n=1) -> vec: ...


class BoxSpace(Space):
    def __init__(self, low: vec, high: vec):
        assert low.shape == high.shape
        assert len(low.shape) == 1

        self.low = low
        self.high = high
        self._size = low.shape[0]

    @property
    def size(self) -> int:
        return self._size

    def sample(self, n=1) -> vec:
        if n == 1:
            return np.random.uniform(self.low, self.high).astype(np.float32)

        return np.random.uniform(self.low, self.high, (n, self._size)).astype(np.float32)


class DiscreteSpace(Space):
    def __init__(self, size: int):
        self._size = size

    @property
    def size(self) -> int:
        return self._size

    def sample(self, n=1) -> vec:
        return np.random.choice(self._size, n)
