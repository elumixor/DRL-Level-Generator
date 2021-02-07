from abc import abstractmethod, ABC

import torch

from .v_estimator import VEstimator


class QEstimator(VEstimator, ABC):
    @abstractmethod
    def get_state_q_values(self, state: torch.Tensor) -> torch.Tensor:
        ...

    def get_state_value(self, state: torch.Tensor):
        return self.get_state_q_values(state).max(dim=-1)[0]
