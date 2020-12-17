import torch
from torch.optim import Adam

from RL.utils import nn_from_layout, bootstrap
from configuration.layout_configuration import LayoutConfiguration
from .vpg_agent import VPGAgent

discounting = 1

test_input = torch.tensor([1], dtype=torch.float, device='cuda')


class A2CAgentSeparate(VPGAgent):

    def __init__(self, actor_layout: LayoutConfiguration, critic_layout: LayoutConfiguration, lr_actor=0.01, lr_critic=0.005):
        super().__init__(actor_layout, lr_actor)
        self.critic = nn_from_layout(critic_layout).cuda()
        self.optim_critic = Adam(self.critic.parameters(), lr=lr_critic)

    def train(self, training_data):
        loss_actor = 0
        loss_critic = 0
        total_len = 0

        for states, actions, rewards, next_states in training_data:
            values = self.critic(states)

            last_state = next_states[-1].unsqueeze(0)
            last_value = self.critic(last_state).item()
            next_values = bootstrap(rewards, last_value, discounting)

            advantage = (next_values - values).flatten()

            loss_critic = loss_critic + .5 * (advantage ** 2).sum()

            probabilities = self.actor(states).softmax(-1)
            probabilities = probabilities[range(states.shape[0]), actions.flatten()]
            loss_actor = loss_actor + (-probabilities.log() * advantage.detach()).sum()

            total_len += states.shape[0]

        loss_actor = loss_actor / total_len
        loss_critic = loss_critic / total_len

        self.optimizer.zero_grad()
        loss_actor.backward()
        self.optimizer.step()

        self.optim_critic.zero_grad()
        loss_critic.backward()
        self.optim_critic.step()
