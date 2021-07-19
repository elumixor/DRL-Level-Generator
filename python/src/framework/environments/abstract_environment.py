import abc
from typing import Tuple

from torch import Tensor


class AbstractEnvironment(abc.ABC):
    @abc.abstractmethod
    def transition(self, state: Tensor, action: int) -> Tuple[Tensor, float, bool]:
        """
        Applies an action in a state, and returns the next state, reward, and done flag
        :param state: State
        :param action: Action
        :return: Tuple (next_state, reward, done)
        """
        pass
