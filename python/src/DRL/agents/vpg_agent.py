from typing import List

import matplotlib.pyplot as plt
import numpy as np
import torch

from DRL import Episode
from DRL.utils import nn_from_layout, rewards_to_go, normalize
from configuration.layout_configuration import LayoutConfiguration
from utilities import log
from .agent import Agent

plt.ion()
plt.show()

discounting = 0.99


class VPGAgent(Agent):
    def __init__(self, actor_layout: LayoutConfiguration):
        self._actor: torch.nn.Module = nn_from_layout(actor_layout).cuda()
        self.optim_actor = torch.optim.Adam(self._actor.parameters(), lr=0.01)
        self.epoch = 0
        super().__init__()

    @property
    def actor(self) -> torch.nn.Module:
        return self._actor

    def train(self, training_data: List[Episode]):
        loss_actor = 0
        total_len = 0

        total_rewards = []

        for states, actions, rewards, next_states in training_data:
            weights = rewards_to_go(rewards, discounting).flatten()
            weights = normalize(weights)

            probabilities = self._actor(states).softmax(-1)
            probabilities = probabilities[range(states.shape[0]), actions.flatten()]
            loss_actor -= (probabilities.log() * weights).sum()

            total_len += states.shape[0]

            total_rewards.append(rewards.sum())

        loss_actor = loss_actor / total_len

        self.optim_actor.zero_grad()
        loss_actor.backward()
        self.optim_actor.step()

        log(f'[Epoch:\t{self.epoch}]:\t{torch.tensor(total_rewards).mean()}')
        self.epoch += 1

        plt.clf()
        p_left_x = self._actor(torch.from_numpy(np.linspace(-1, 1, 10)).float().cuda().unsqueeze(-1)) \
                       .softmax(-1)[:, 0].cpu().detach().numpy()
        plt.plot(np.linspace(-1, 1, 10), p_left_x)
        plt.ylim([0, 1])
        plt.draw()
        plt.pause(0.001)
