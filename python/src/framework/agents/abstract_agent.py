import abc

from torch import Tensor


class AbstractAgent(abc.ABC):
    @abc.abstractmethod
    def get_action(self, state: Tensor) -> Tensor:
        """
        Returns the action for a state
        :param state: State
        :return: Action
        """
        pass
