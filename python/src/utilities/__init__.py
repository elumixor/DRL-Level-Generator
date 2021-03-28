import functools
import sys
from datetime import timedelta

import torch
from numba import njit
from scipy.stats import skewnorm

from .buffer import Buffer
from .event import Event
from .logging import *
from .math_utilities import *


def eprint(*args):
    print(*args, file=sys.stderr)


def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"{func.__name__}()")
        func(*args, **kwargs)

    return wrapper


def clamp(value, _min, _max):
    return max(_min, min(value, _max))


def time_string(seconds):
    return str(timedelta(seconds=round(seconds)))


@torch.no_grad()
def get_total_gradient(nn):
    total_grad = 0.0
    count = 0

    for p in nn.parameters():
        total_grad += p.grad.data.abs().mean()
        count += 1

    return total_grad / count


@njit
def get_trajectory_reward(env, agent, max_length):
    total_reward = 0

    state = env.reset()
    for _ in range(max_length):
        action = agent.get_action(state)
        state, reward, done = env.step(action)
        total_reward += reward
        if done:
            break

    return total_reward


def weight_skills(skills, mean, std, skew) -> np.ndarray:
    cdf_0 = skewnorm.cdf(0, skew, loc=mean, scale=std)
    cdf_1 = skewnorm.cdf(1, skew, loc=mean, scale=std)
    diff = cdf_1 - cdf_0

    weights = skewnorm.pdf(skills, skew, loc=mean, scale=std) / diff
    return weights / weights.sum()


class time_section:
    def __init__(self):
        self.start_time: float

    def __enter__(self):
        self.start_time = datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = datetime.now()
        total = end_time - self.start_time
        print(total)
