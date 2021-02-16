import itertools

import torch
from torch.nn import Identity, Linear, Sequential, ReLU

from serialization import auto_saved, auto_serialized
from .agent import Agent
from ..analysis import auto_logged
from ..utils import MLP, map_transitions, bootstrap


@auto_logged(plot_names=["mean_total_reward", "loss_actor", "loss_critic", "loss_entropy"],
             print_names=["mean_total_reward"])
@auto_saved
@auto_serialized(skip=["base", "actor_head", "critic_head"])
class A2CAgent(Agent):
    def __init__(self, env, hidden_sizes=None, lr=0.01, discount=0.99, time_delay=10, critic_loss_weight=0.5,
                 entropy_loss_weight=0.01):
        if hidden_sizes is None:
            hidden_sizes = [8, 6]

        observation_size = env.observation_size
        self.action_size = env.action_size

        last_size = observation_size
        if len(hidden_sizes) > 0:
            last_size = hidden_sizes[-1]
            self.base = MLP(observation_size, last_size, hidden_sizes[:-1])
        else:
            self.base = Identity()

        self.actor_head = Linear(last_size, self.action_size)
        self.critic_head = Linear(last_size, 1)

        self.actor = Sequential(self.base, ReLU(), self.actor_head)
        self.critic = Sequential(self.base, ReLU(), self.critic_head)

        self.optim = torch.optim.Adam(itertools.chain(self.actor.parameters(), self.critic_head.parameters()), lr=lr)

        # self.actor = MLP(observation_size, self.action_size, [8, 8])
        # self.critic = MLP(observation_size, 1, [8, 8])
        # self.optim = torch.optim.Adam(itertools.chain(self.actor.parameters(), self.critic.parameters()), lr=lr)

        self.discount = discount
        self.time_delay = time_delay
        self.critic_loss_weight = critic_loss_weight
        self.entropy_loss_weight = entropy_loss_weight

        self.mean_total_reward = 0.0
        self.loss_actor = 0.0
        self.loss_critic = 0.0
        self.loss_entropy = 0.0

    def get_action(self, observation):
        with torch.no_grad():
            logits = self.actor(observation)
            distribution = torch.distributions.Categorical(logits=logits)
            action = distribution.sample([1])
            return action

    def update(self, trajectories):
        loss_actor = 0.0
        loss_critic = 0.0
        entropy_loss = 0.0

        total_len = 0

        total_reward = 0.0
        for transitions in trajectories:
            states, actions, rewards, done, next_states = map_transitions(transitions)

            v = self.critic(states).flatten()
            v_next = self.critic(next_states).flatten()

            y = bootstrap(rewards, v_next, self.time_delay, self.discount)
            advantages = y - v
            loss_critic = loss_critic + (advantages ** 2).sum()

            probabilities = self.actor(states).softmax(-1)
            probabilities = probabilities[range(actions.shape[0]), actions.flatten()]
            loss_actor = loss_actor - (probabilities.log() * advantages.flatten().detach()).sum()

            entropy_loss = entropy_loss + (probabilities * probabilities.log()).sum()

            total_len += states.shape[0]
            total_reward += rewards.sum().item()

        loss_actor = loss_actor / total_len
        loss_critic = loss_critic / total_len
        entropy_loss = entropy_loss / total_len

        loss = loss_actor + self.critic_loss_weight * loss_critic + self.entropy_loss_weight * entropy_loss

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        # For logging
        self.mean_total_reward = total_reward / len(trajectories)

        self.loss_actor = loss_actor.item()
        self.loss_critic = loss_critic.item()
        self.loss_entropy = entropy_loss.item()
