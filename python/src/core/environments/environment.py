from abc import ABC, abstractmethod
from typing import Tuple, Optional

import torch


class Environment(ABC):
    @abstractmethod
    def render(self):
        """
        Renders the current observation
        """

    @property
    @abstractmethod
    def state_size(self) -> int:
        """
        Size of the observation
        """

    @property
    @abstractmethod
    def action_size(self) -> int:
        """
        Size of the action
        """

    @property
    def observation_size(self) -> int:
        """
        Size of the observation. Defaults to the size of the observation
        """
        return self.state_size

    @abstractmethod
    def reset(self, difficulty: Optional[float] = None, seed: Optional[float] = None) -> torch.Tensor:
        """
        Resets the environment to a starting observation. Returns that starting observation

        :param difficulty: Difficulty to generate the observation. If None, will use the last difficulty specified
        :param seed: Random seed to generate environment. Can be set manually to produce deterministic results
        :returns: Starting observation
        """

    @abstractmethod
    def transition(self, action: torch.Tensor) -> Tuple[torch.Tensor, float, bool]:
        """
        Transitions from the previous observation to the next observation, given the agent's action

        :returns: Next observation, reward, done
        """

    @abstractmethod
    def get_observation(self, state):
        """
        For the given observation, returns an observation
        """
        return state
