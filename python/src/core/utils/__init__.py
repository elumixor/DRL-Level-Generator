import torch

from .auto_eval import auto_eval
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

    states = torch.stack(states).detach().cuda()
    actions = torch.stack(actions).detach().cuda()
    rewards = torch.tensor(rewards).detach().cuda()
    done = torch.tensor(done).cuda()
    next_states = torch.stack(next_states).detach().cuda()

    return states, actions, rewards, done, next_states
