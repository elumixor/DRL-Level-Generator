from typing import List

import matplotlib.pyplot as plt
import numpy as np
import torch

from RL import Episode
from RL.utils import nn_from_layout, rewards_to_go, running_average, normalize
from configuration.layout_configuration import LayoutConfiguration
from utilities import log, Buffer
from .agent import Agent

plt.ion()

discounting = 1

test_input = torch.tensor([1], dtype=torch.float, device='cuda')


class VPGAgent(Agent):
    def __init__(self, actor_layout: LayoutConfiguration):
        self._actor: torch.nn.Module = nn_from_layout(actor_layout).cuda()
        self.optim_actor = torch.optim.Adam(self._actor.parameters(), lr=0.01)
        self.epoch = 0
        self.mean_total_rewards = Buffer(100)

        self.fig, self.axs = plt.subplots(3, figsize=(6, 8))

        # Split the spawning field into ten buckets
        self.spawns = []
        self.positions = []

        print("Actor NN initialized")
        for p in self._actor.parameters():
            print(p)

        print(str(test_input) + " is mapped onto " + str(self._actor(test_input)))

        plt.show()

    @property
    def actor(self) -> torch.nn.Module:
        return self._actor

    def train(self, training_data: List[Episode]):
        loss_actor = 0
        total_len = 0

        total_rewards = []

        # log(f'[Epoch:\t{self.epoch}]:\tTRAINING DATA START')
        # i = 0
        for states, actions, rewards, next_states in training_data:
            weights = rewards_to_go(rewards, discounting).flatten()
            weights = normalize(weights)  # does not work correctly when normalization is applied. Why?

            probabilities = self._actor(states).softmax(-1)
            probabilities = probabilities[range(states.shape[0]), actions.flatten()]
            loss_actor -= (probabilities.log() * weights).sum()

            total_len += states.shape[0]

            total_rewards.append(rewards.sum())

            # DEBUG INFO
            # Count the add the spawning place
            start_x = states[0].cpu().item()
            self.spawns.append(start_x)
            self.positions += states.flatten().cpu().tolist()

        loss_actor = loss_actor / total_len

        self.optim_actor.zero_grad()
        loss_actor.backward()
        self.optim_actor.step()

        print(str(test_input) + " is mapped onto " + str(self._actor(test_input)))

        mean_total_reward = float(torch.tensor(total_rewards).mean().item())
        self.mean_total_rewards.push(mean_total_reward)

        log(f'[Epoch:\t{self.epoch}]:\t{mean_total_reward}')
        self.epoch += 1
        # Clear already plotted data
        self.axs[0].clear()
        self.axs[1].clear()
        self.axs[2].clear()

        # Probability of going left
        x = np.linspace(-5, 5, 10)
        p_left_x = self._actor(torch.from_numpy(x).float().cuda().unsqueeze(-1)) \
                       .softmax(-1)[:, 0].cpu().detach().numpy()
        x_opt = x[np.argmin(np.abs(p_left_x - .5))]
        self.axs[0].plot([-5, 5], [.5, .5], color="red", linewidth=.3)
        self.axs[0].plot([x_opt, x_opt], [0, 1], color="red", linewidth=.3)
        self.axs[0].plot(x, p_left_x)
        self.axs[0].set_ylim([0, 1])
        self.axs[0].grid(color='black', linestyle='-', linewidth=.1)

        # Mean total reward for all episodes in an epoch, and the running average
        self.axs[1].plot([x for x in self.mean_total_rewards])
        self.axs[1].plot(running_average([x for x in self.mean_total_rewards]))

        # Ocurrence frequency
        self.axs[2].hist(self.positions, bins=np.arange(-5, 6, .5), label="Times been in position")

        # Spawn frequency
        self.axs[2].hist(self.spawns, bins=np.arange(-5, 6, .5), label="Times spawned at position")
        self.axs[2].legend()

        self.axs[0].set_title("Probability of going left")
        self.axs[1].set_title("Mean total episode reward")
        self.axs[2].set_title("Times been in position")

        plt.draw()
        plt.tight_layout()
        plt.pause(0.001)