from abc import ABC, abstractmethod

import torch

from ..trajectory import Trajectory


class VEstimator(ABC):
    @abstractmethod
    def get_state_value(self, state: torch.Tensor):
        ...

    def get_trajectory_values(self, trajectory: Trajectory):
        return torch.tensor([self.get_state_value(state) for state, *_ in trajectory])
