from typing import List

import matplotlib.pyplot as plt
import numpy as np
import torch

from DRL import Episode
from DRL.utils import nn_from_layout, rewards_to_go, normalize, running_average
from configuration.layout_configuration import LayoutConfiguration
from utilities import log
from .agent import Agent

plt.ion()

discounting = 0.99


class VPGAgent(Agent):
    def __init__(self, actor_layout: LayoutConfiguration):
        self._actor: torch.nn.Module = nn_from_layout(actor_layout).cuda()
        self.optim_actor = torch.optim.Adam(self._actor.parameters(), lr=0.05)
        self.epoch = 0
        self.mean_total_rewards = []
        self.plot_last_rewards_count = 100

        self.fig, self.axs = plt.subplots(2)


        self.axs[0].set_title("Probabilities")
        self.axs[1].set_title("Mean total episode reward")
        plt.show()

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
            # weights = normalize(weights)  # does not work correctly when normalization is applied. Why?

            probabilities = self._actor(states).softmax(-1)
            probabilities = probabilities[range(states.shape[0]), actions.flatten()]
            loss_actor -= (probabilities.log() * weights).sum()

            total_len += states.shape[0]

            total_rewards.append(rewards.sum())

        loss_actor = loss_actor / total_len

        self.optim_actor.zero_grad()
        loss_actor.backward()
        self.optim_actor.step()

        mean_total_reward = float(torch.tensor(total_rewards).mean().item())
        self.mean_total_rewards.append(mean_total_reward)

        if len(self.mean_total_rewards) > self.plot_last_rewards_count:
            self.mean_total_rewards.pop(0)

        log(f'[Epoch:\t{self.epoch}]:\t{mean_total_reward}')
        self.epoch += 1

        x = np.linspace(-3, 3, 10)
        p_left_x = self._actor(torch.from_numpy(x).float().cuda().unsqueeze(-1)) \
                       .softmax(-1)[:, 0].cpu().detach().numpy()

        self.axs[0].clear()
        self.axs[1].clear()

        self.axs[0].plot(x, p_left_x)
        self.axs[0].set_ylim([0, 1])

        self.axs[1].plot(self.mean_total_rewards)
        self.axs[1].plot(running_average(self.mean_total_rewards))

        plt.draw()
        plt.pause(0.001)
