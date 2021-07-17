import abc

from torch import Tensor

from .abstract_agent import AbstractAgent


class AbstractQAgent(AbstractAgent, abc.ABC):
    """
    Agent, that can provide Q-values for the state
    """

    @abc.abstractmethod
    def get_q_values(self, state: Tensor) -> Tensor:
        """
        Returns the Q-values for the actions in the state
        :param state: State
        :return: Q-values for the actions, shape (num_states, num_actions)
        """
        pass
