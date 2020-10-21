from abc import abstractmethod
from typing import List

import torch

from DRL.agent import Episode


class Agent:
    @abstractmethod
    def train(self, training_data: List[Episode]):
        pass

    @property
    @abstractmethod
    def actor(self) -> torch.nn.Module:
        pass
