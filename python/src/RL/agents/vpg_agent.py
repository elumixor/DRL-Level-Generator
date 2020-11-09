from typing import List

import torch

from RL import Episode
from RL.utils import nn_from_layout, discounted_rewards
from configuration.layout_configuration import LayoutConfiguration
from utilities import Buffer, np
from utilities.logging.left_right_plotter import LeftRightPlotter
from .agent import Agent

discounting = .99

test_input = torch.tensor([1], dtype=torch.float, device='cuda')


class VPGAgent(Agent):

    def __init__(self, actor_layout: LayoutConfiguration, plotter_class=LeftRightPlotter):
        self._actor: torch.nn.Module = nn_from_layout(actor_layout).cuda()
        self.optim_actor = torch.optim.Adam(self._actor.parameters(), lr=0.1)
        self.epoch = 0
        self.mean_total_rewards = Buffer(100)

        # Split the spawning field into ten buckets
        self.spawns = []
        self.positions = []

        self.plotter = plotter_class(frequency=20)

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

        self.optim_actor.zero_grad()
        loss_actor.backward()
        self.optim_actor.step()

        # Also plot the probability of going left
        if self.plotter is LeftRightPlotter:
            x = np.linspace(-5, 5, 100)
            p_left_x = self._actor(torch.from_numpy(x).float().unsqueeze(-1)) \
                           .softmax(-1)[:, 0].detach().numpy()
            self.plotter.update(training_data, p_left_x=(x, p_left_x))
        else:
            self.plotter.update(training_data)
