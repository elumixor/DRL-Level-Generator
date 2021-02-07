import numpy as np
import torch

from serialization import auto_serialized, auto_saved
from .agent import Agent
from ..analysis import auto_logged
from ..utils import MLP, map_transitions, discounted_rewards


@auto_logged(plot_names=["mean_total_reward"], print_names=["mean_total_reward"])
@auto_saved
@auto_serialized
class VPGAgent(Agent):
    def __init__(self, env, hidden_sizes=None, lr=0.01,
                 discount=0.99):
        if hidden_sizes is None:
            hidden_sizes = [8, 8]

        observation_size = env.observation_size
        self.action_size = env.action_size

        self.actor = MLP(observation_size, self.action_size, hidden_sizes)
        self.optim = torch.optim.Adam(self.actor.parameters(), lr=lr)

        self.discount = discount
        self.mean_total_reward = 0.0

    def get_action(self, observation):
        logits = self.actor(observation)
        distribution = torch.distributions.Categorical(logits=logits)
        action = distribution.sample([1]).detach()
        return action

    def update(self, trajectories):
        loss = 0
        total_len = 0
        total_rewards = []

        for transitions in trajectories:
            states, actions, rewards, done, next_states = map_transitions(transitions)

            weights = discounted_rewards(rewards, self.discount).flatten()

            probabilities = self.actor(states).softmax(-1)
            probabilities = probabilities[range(states.shape[0]), actions.flatten()]
            loss = loss + (-probabilities.log() * weights).sum()
            total_len += weights.shape[0]

            total_rewards.append(rewards.sum().item())

        loss = loss / total_len

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        self.mean_total_reward = np.mean(total_rewards)
