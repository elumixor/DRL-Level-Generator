from abc import ABC, abstractmethod

from torch import Tensor


class State(Tensor, ABC):
    @property
    @abstractmethod
    def embedding(self):
        pass

    @embedding.setter
    @abstractmethod
    def embedding(self, value: Tensor):
        pass
