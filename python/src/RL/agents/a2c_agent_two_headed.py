from itertools import chain

import matplotlib.pyplot as plt
import numpy as np
import torch

from RL.utils import nn_from_layout, bootstrap
from utilities import running_average
from configuration.layout_configuration import LayoutConfiguration
from utilities import Buffer
from .agent import Agent

test_input = torch.tensor([1], dtype=torch.float, device='cuda')

discounting = 0.99


class A2CAgentTwoHeaded(Agent):

    def __init__(self, base_layout: LayoutConfiguration, actor_head_layout: LayoutConfiguration, critic_head_layout: LayoutConfiguration):
        self.epoch = 0
        self.mean_total_rewards = Buffer(100)

        self.base = nn_from_layout(base_layout).cuda()
        self.critic_head = nn_from_layout(critic_head_layout).cuda()
        self.actor_head = nn_from_layout(actor_head_layout).cuda()

        self._actor = torch.nn.Sequential(self.base, self.actor_head).cuda()
        self.critic = torch.nn.Sequential(self.base, self.critic_head).cuda()

        self.optim = torch.optim.Adam(chain(self.base.parameters(), self.actor_head.parameters(), self.critic_head.parameters()), lr=0.01)
        self.fig, self.axs = plt.subplots(2, figsize=(6, 6))

        print("Actor initialized")
        print(self._actor)

        print("Critic initialized")
        print(self.critic)

    @property
    def actor(self) -> torch.nn.Module:
        return self._actor

    def train(self, training_data):
        loss = 0
        total_len = 0

        total_rewards = []

        for states, actions, rewards, next_states in training_data:
            values = self.critic(states)

            last_state = next_states[-1].unsqueeze(0)
            last_value = self.critic(last_state).item()
            next_values = bootstrap(rewards, last_value, discounting)

            advantage = (next_values - values).flatten()

            loss_critic = .5 * (advantage ** 2).sum()

            probabilities = self.actor(states).softmax(-1)
            probabilities = probabilities[range(states.shape[0]), actions.flatten()]
            loss_actor = -(probabilities.log() * advantage.detach()).sum()

            loss = loss + loss_critic + loss_actor

            total_len += states.shape[0]

            total_rewards.append(rewards.sum())

        loss = loss / total_len

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        mean_total_reward = float(torch.tensor(total_rewards).mean().item())
        self.mean_total_rewards.push(mean_total_reward)

        self.epoch += 1

        # TODO: log and plot results
        # Clear already plotted data
        self.axs[0].clear()
        self.axs[1].clear()

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
        epochs = [x + max(self.epoch - len(self.mean_total_rewards), 0) for x in range(len(self.mean_total_rewards))]
        self.axs[1].plot(epochs, [x for x in self.mean_total_rewards])
        self.axs[1].plot(epochs, running_average([x for x in self.mean_total_rewards]))
        self.axs[1].grid(color='black', linestyle='-', linewidth=.1)

        self.axs[0].set_title("Probability of going left")
        self.axs[1].set_title("Mean total episode reward")

        plt.draw()
        plt.tight_layout()
        plt.pause(0.001)
