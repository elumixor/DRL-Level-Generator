from abc import ABC, abstractmethod
from typing import Tuple, Any

import numpy as np


class BaseEnvironment(ABC):

    def seed(self, seed):
        pass

    def render(self):
        pass

    @property
    @abstractmethod
    def observation_space(self):
        pass

    @property
    @abstractmethod
    def action_space(self):
        pass

    @abstractmethod
    def reset(self) -> np.ndarray:
        """
        Resets the environment to a starting state. Returns that starting state
        :rtype: Starting state
        """
        pass

    @abstractmethod
    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, Any]:
        """
        Performs a step into an environment
        :rtype: Returns new state, reward and flag if is done,
        and something else which I don't know that is there to be compatible with OpenAI gym API
        """
        pass
