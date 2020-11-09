from typing import List

import torch

from RL import Episode
from RL.utils import nn_from_layout, discounted_rewards
from configuration.layout_configuration import LayoutConfiguration
from .agent import Agent

discounting = .99

test_input = torch.tensor([1], dtype=torch.float, device='cuda')


class VPGAgent(Agent):

    def __init__(self, actor_layout: LayoutConfiguration, lr=0.01):
        self._actor = nn_from_layout(actor_layout).cuda()
        self.optimizer = torch.optim.Adam(self._actor.parameters(), lr=lr)

    @property
    def actor(self) -> torch.nn.Module:
        return self._actor

    def train(self, training_data: List[Episode]):
        loss_actor = 0
        total_len = 0

        for states, actions, rewards, next_states in training_data:
            weights = discounted_rewards(rewards, discounting).flatten()

            probabilities = self._actor(states).softmax(-1)
            probabilities = probabilities[range(states.shape[0]), actions.flatten()]
            loss_actor = loss_actor + (-probabilities.log() * weights).sum()
            total_len += weights.shape[0]

        loss_actor = loss_actor / total_len

        self.optimizer.zero_grad()
        loss_actor.backward()
        self.optimizer.step()
