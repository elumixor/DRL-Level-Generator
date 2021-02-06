import torch

from .epsilon_decay import EpsilonDecay
from .mlp import mlp as MLP


def bootstrap(rewards, last, discounting=0.99):
    res = torch.zeros_like(rewards)
    for i in reversed(range(rewards.shape[0])):
        last = res[i] = rewards[i] + discounting * last
    return res


def discounted_rewards(rewards, discounting=0.99):
    res = torch.zeros_like(rewards)
    last = 0.
    for i in reversed(range(rewards.shape[0])):
        last = res[i][0] = rewards[i][0] + discounting * last

    return res


def map_transitions(transitions):
    states, actions, rewards, done, next_states = zip(*transitions)

    states = torch.stack(states).detach()
    actions = torch.stack(actions).detach()
    rewards = torch.tensor(rewards).detach()
    done = torch.tensor(done)
    next_states = torch.stack(next_states).detach()

    return states, actions, rewards, done, next_states
