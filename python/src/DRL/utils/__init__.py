import torch

from .nn_from_layout import nn_from_layout


def bootstrap(rewards, last, discounting=0.99):
    res = torch.zeros_like(rewards)
    for i in reversed(range(rewards.shape[0])):
        last = res[i] = rewards[i] + discounting * last
    return res


def normalize(tensor):
    return (tensor - tensor.mean()) / tensor.std()


def rewards_to_go(rewards, discounting=0.99):
    res = torch.zeros_like(rewards)
    last = 0.
    for i in reversed(range(rewards.shape[0])):
        last = res[i][0] = rewards[i][0] + discounting * last

    return res
