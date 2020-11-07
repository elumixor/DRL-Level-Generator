from abc import abstractmethod
from typing import List

import torch
from RL import Episode


class Agent:
    @abstractmethod
    def train(self, training_data: List[Episode]) -> None:
        pass

    @property
    @abstractmethod
    def actor(self) -> torch.nn.Module:
        pass
