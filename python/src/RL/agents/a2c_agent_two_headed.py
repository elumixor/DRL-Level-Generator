from itertools import chain

import matplotlib.pyplot as plt
import numpy as np
import torch

from RL.utils import nn_from_layout, running_average
from configuration.layout_configuration import LayoutConfiguration
from utilities import log
from .agent import Agent

test_input = torch.tensor([1], dtype=torch.float, device='cuda')


class A2CAgentTwoHeaded(Agent):

    def __init__(self, base_layout: LayoutConfiguration, actor_head_layout: LayoutConfiguration, critic_head_layout: LayoutConfiguration):
        self.base = nn_from_layout(base_layout)
        self.critic_head = nn_from_layout(critic_head_layout)
        self.actor_head = nn_from_layout(actor_head_layout)

        self._actor = torch.nn.Sequential(self.base, self.actor_head)
        self.critic = torch.nn.Sequential(self.base, self.critic_head)

        self.optim = torch.optim.Adam(chain(self.base.parameters(), self.actor_head.parameters(), self.critic_head.parameters()), lr=0.01)
        self.fig, self.axs = plt.subplots(2, figsize=(6, 6))

        print("Actor NN initialized")
        for p in self._actor.parameters():
            print(p)

        print(str(test_input) + " is mapped onto " + str(self._actor(test_input)))

    @property
    def actor(self) -> torch.nn.Module:
        return self._actor

    def train(self, training_data):
        loss_actor = 0
        total_len = 0

        total_rewards = []

        # for states, actions, rewards, next_states in training_data:
        #     weights = rewards_to_go(rewards, discounting).flatten()
        #     weights = normalize(weights)  # does not work correctly when normalization is applied. Why?
        #
        #     probabilities = self._actor(states).softmax(-1)
        #     probabilities = probabilities[range(states.shape[0]), actions.flatten()]
        #     loss_actor -= (probabilities.log() * weights).sum()
        #
        #     total_len += states.shape[0]
        #
        #     total_rewards.append(rewards.sum())
        #
        #     # DEBUG INFO
        #     # Count the add the spawning place
        #     start_x = states[0].cpu().item()
        #     self.spawns.append(start_x)
        #     self.positions += states.flatten().cpu().tolist()
        #
        # loss_actor = loss_actor / total_len
        #
        # self.optim_actor.zero_grad()
        # loss_actor.backward()
        # self.optim_actor.step()

        print(str(test_input) + " is mapped onto " + str(self._actor(test_input)))

        mean_total_reward = float(torch.tensor(total_rewards).mean().item())
        self.mean_total_rewards.push(mean_total_reward)

        log(f'[Epoch:\t{self.epoch}]:\t{mean_total_reward}')
        self.epoch += 1
        # Clear already plotted data
        self.axs[0].clear()
        self.axs[1].clear()
        # self.axs[2].clear()

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
        # self.axs[2].hist(self.positions, bins=np.arange(-5, 6, .5), label="Times been in position")

        # Spawn frequency
        # self.axs[2].hist(self.spawns, bins=np.arange(-5, 6, .5), label="Times spawned at position")
        # self.axs[2].legend()

        self.axs[0].set_title("Probability of going left")
        self.axs[1].set_title("Mean total episode reward")
        # self.axs[2].set_title("Times been in position")

        plt.draw()
        plt.tight_layout()
        plt.pause(0.001)
