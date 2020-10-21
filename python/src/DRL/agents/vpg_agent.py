from typing import List

import torch

from DRL import Episode
from DRL.utils import nn_from_layout
from configuration.layout_configuration import LayoutConfiguration
from .agent import Agent


class VPGAgent(Agent):
    def __init__(self, actor_layout: LayoutConfiguration):
        self._actor = nn_from_layout(actor_layout)
        super().__init__()

    @property
    def actor(self) -> torch.nn.Module:
        return self._actor

    def train(self, training_data: List[Episode]):
        pass
