from abc import ABC, abstractmethod

import torch


class Actor(ABC):
    @abstractmethod
    def get_action(self, observation: torch.Tensor) -> torch.Tensor:
        """
        Use the agent to infer an action, given the observation
        """
