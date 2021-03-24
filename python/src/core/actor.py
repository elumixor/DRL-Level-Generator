from abc import ABC, abstractmethod

import torch


class Actor(ABC):
    def __init__(self, env):
        self.env = env

    @abstractmethod
    def get_action(self, observation: torch.Tensor) -> torch.Tensor:
        """
        Use the agent to infer an action, given the observation
        """
