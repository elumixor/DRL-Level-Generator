import torch
import torch.nn as nn
from torch.distributions import Uniform

from layout import action_size, state_size

hidden_size = 20

# Actor maps state to probabilities of taking action
actor = nn.Sequential(
    nn.Linear(state_size, hidden_size),
    nn.ReLU(),
    nn.Linear(hidden_size, hidden_size),
    nn.ReLU(),
    nn.Linear(hidden_size, action_size)).cuda()

# Critic maps state to value of the state
critic = nn.Sequential(
    nn.Linear(state_size, hidden_size),
    nn.ReLU(),
    nn.Linear(hidden_size, hidden_size),
    nn.ReLU(),
    nn.Linear(hidden_size, 1)).cuda()


class Agent:
    def __init__(self):
        pass

    def infer(self, state: torch.tensor) -> torch.tensor:
        p_tap = actor(state.cuda()).cpu()
        sampled = Uniform(torch.tensor(0.0), torch.tensor(1.0)).sample()
        return torch.tensor(-1 if sampled < p_tap else 1)

    def train(self, training_data):
        (states, actions, rewards) = training_data


agent = Agent()
