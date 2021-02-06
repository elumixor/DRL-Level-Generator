from itertools import chain

import torch
from RL.utils import nn_from_layout, discounted_rewards
from configuration.layout_configuration import LayoutConfiguration

from utilities import Buffer
from .agent import Agent

test_input = torch.tensor([1], dtype=torch.float, device='cuda')

discounting = 0.99


class A2CAgentTwoHeaded(Agent):

    def __init__(self, base_layout: LayoutConfiguration, actor_head_layout: LayoutConfiguration, critic_head_layout: LayoutConfiguration,
                 lr=0.01, loss_critic_coeff=0.001):
        self.loss_critic_coeff = loss_critic_coeff
        self.epoch = 0
        self.mean_total_rewards = Buffer(100)

        self.base = nn_from_layout(base_layout).cuda()
        self.actor_head = nn_from_layout(actor_head_layout).cuda()
        self.critic_head = nn_from_layout(critic_head_layout).cuda()

        self._actor = torch.nn.Sequential(self.base, self.actor_head).cuda()
        self.critic = torch.nn.Sequential(self.base, self.critic_head).cuda()

        self.optim = torch.optim.Adam(chain(self.actor.parameters(), self.critic_head.parameters()), lr=lr)

    @property
    def actor(self) -> torch.nn.Module:
        return self._actor

    def train(self, training_data):
        loss = 0
        total_len = 0

        for states, actions, rewards, next_states in training_data:
            values = self.critic(states)

            target_values = discounted_rewards(rewards, discounting)
            advantages = (target_values - values)

            loss_critic = self.loss_critic_coeff * (advantages ** 2).sum()

            probabilities = self.actor(states).softmax(-1)
            probabilities = probabilities[range(states.shape[0]), actions.flatten()]
            loss_actor = -(probabilities.log() * advantages.flatten().detach()).sum()

            loss = loss + loss_critic + loss_actor

            total_len += states.shape[0]

        loss = loss / total_len

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()
