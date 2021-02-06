from abc import ABC, abstractmethod
from typing import Tuple

import torch


class Environment(ABC):
    def seed(self, seed):
        pass

    @abstractmethod
    def render(self):
        pass

    @property
    @abstractmethod
    def observation_size(self) -> int:
        pass

    @property
    @abstractmethod
    def action_size(self) -> int:
        pass

    @abstractmethod
    def reset(self) -> torch.tensor:
        """
        Resets the environment to a starting state. Returns that starting state
        :rtype: Starting state
        """
        pass

    @abstractmethod
    def transition(self, action: torch.tensor) -> Tuple[torch.tensor, float, bool]:
        """
        Transitions from the previous state to the next state, given the agent's action
        :returns: Next state, reward, done
        """
        pass

    @abstractmethod
    def get_observation(self, state):
        pass
