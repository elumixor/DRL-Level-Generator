import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.optim import Adam

from RL.utils import nn_from_layout, bootstrap
from utilities import running_average
from configuration.layout_configuration import LayoutConfiguration
from .vpg_agent import VPGAgent

discounting = 1

test_input = torch.tensor([1], dtype=torch.float, device='cuda')


class A2CAgentSeparate(VPGAgent):

    def __init__(self, actor_layout: LayoutConfiguration, critic_layout: LayoutConfiguration):
        super().__init__(actor_layout)
        self.critic = nn_from_layout(critic_layout).cuda()

        print("Critic NN initialized")
        for p in self.critic.parameters():
            print(p)

        self.optim_critic = Adam(self.critic.parameters(), lr=0.005)

    def train(self, training_data):
        loss_actor = 0
        loss_critic = 0
        total_len = 0

        total_rewards = []

        for states, actions, rewards, next_states in training_data:
            values = self.critic(states)

            last_state = next_states[-1].unsqueeze(0)
            last_value = self.critic(last_state).item()
            next_values = bootstrap(rewards, last_value, discounting)

            advantage = (next_values - values).flatten()

            loss_critic += .5 * (advantage ** 2).sum()

            probabilities = self.actor(states).softmax(-1)
            probabilities = probabilities[range(states.shape[0]), actions.flatten()]
            loss_actor = loss_actor + (-probabilities.log() * advantage.detach()).sum()

            total_len += states.shape[0]

            total_rewards.append(rewards.sum())

        loss_actor = loss_actor / total_len
        loss_critic = loss_critic / total_len

        self.optim_actor.zero_grad()
        loss_actor.backward()
        self.optim_actor.step()

        self.optim_critic.zero_grad()
        loss_critic.backward()
        self.optim_critic.step()

        mean_total_reward = float(torch.tensor(total_rewards).mean().item())
        self.mean_total_rewards.push(mean_total_reward)

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
        epochs = [x + max(self.epoch - len(self.mean_total_rewards), 0) for x in range(len(self.mean_total_rewards))]
        self.axs[1].plot(epochs, [x for x in self.mean_total_rewards])
        self.axs[1].plot(epochs, running_average([x for x in self.mean_total_rewards]))
        self.axs[1].grid(color='black', linestyle='-', linewidth=.1)

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
