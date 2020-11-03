from itertools import chain

import torch

from RL.utils import nn_from_layout
from configuration.layout_configuration import LayoutConfiguration
from . import Agent


class A2CAgentCombined(Agent):
    def __init__(self, base_layout: LayoutConfiguration, actor_layout: LayoutConfiguration, critic_layout: LayoutConfiguration):
        self.base = nn_from_layout(base_layout)
        self.critic_head = nn_from_layout(critic_layout)
        self.actor_head = nn_from_layout(actor_layout)

        self._actor = torch.nn.Sequential(self.base, self.actor_head)
        self.critic = torch.nn.Sequential(self.base, self.critic_head)

        self.optim = torch.optim.Adam(chain(self.base.parameters(), self.actor_head.parameters(), self.critic_head.parameters()), lr=0.01)

    @property
    def actor(self) -> torch.nn.Module:
        return self._actor

    def train(self, training_data):
        pass
