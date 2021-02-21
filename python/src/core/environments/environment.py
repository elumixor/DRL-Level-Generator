from abc import ABC, abstractmethod
from typing import Tuple, Optional

import torch


class Environment(ABC):
    @abstractmethod
    def render(self):
        """
        Renders the current state
        """

    @property
    @abstractmethod
    def state_size(self) -> int:
        """
        Size of the state
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
        Size of the observation. Defaults to the size of the state
        """
        return self.state_size

    @abstractmethod
    def reset(self, difficulty: Optional[float] = None, seed: Optional[float] = None) -> torch.Tensor:
        """
        Resets the environment to a starting state. Returns that starting state

        :param difficulty: Difficulty to generate the state. If None, will use the last difficulty specified
        :param seed: Random seed to generate environment. Can be set manually to produce deterministic results
        :returns: Starting state
        """

    @abstractmethod
    def transition(self, action: torch.tensor) -> Tuple[torch.tensor, float, bool]:
        """
        Transitions from the previous state to the next state, given the agent's action

        :returns: Next state, reward, done
        """

    @abstractmethod
    def get_observation(self, state):
        """
        For the given state, returns an observation
        """
        return state
