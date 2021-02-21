import torch

from serialization import auto_serialized, auto_saved
from .agent import Agent
from ..analysis import auto_logged
from ..utils import MLP, map_transitions, discounted_rewards


@auto_logged("train", plot_names=["total_reward", "loss"], print_names=["total_reward"])
@auto_saved
@auto_serialized
class VPGAgent(Agent):
    def __init__(self, env, hidden_sizes=None, lr=0.01, discount=0.99):
        if hidden_sizes is None:
            hidden_sizes = [8, 8]

        observation_size = env.observation_size
        self.action_size = env.action_size

        self.actor = MLP(observation_size, self.action_size, hidden_sizes)
        self.optim = torch.optim.Adam(self.actor.parameters(), lr=lr)

        self.discount = discount
        self.mean_total_reward = 0.0
        self.loss = 0.0

    def get_action(self, observation):
        with torch.no_grad():
            logits = self.actor(observation)
            distribution = torch.distributions.Categorical(logits=logits)
            action = distribution.sample([1])
            return action

    def train(self, trajectories):
        loss = 0.0
        total_len = 0
        total_reward = 0.0

        for transitions in trajectories:
            states, actions, rewards, done, next_states = map_transitions(transitions)
            _discounted_rewards = discounted_rewards(rewards, self.discount).flatten()

            probabilities = self.actor(states).softmax(-1)
            probabilities = probabilities[range(states.shape[0]), actions.flatten()]
            loss = loss - (probabilities.log() * _discounted_rewards).sum()

            total_len += _discounted_rewards.shape[0]
            total_reward += rewards.sum().item()

        loss = loss / total_len

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

        self.mean_total_reward = total_reward / len(trajectories)

        self.loss = loss.item()
