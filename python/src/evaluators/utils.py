import numpy as np
import torch
from numba import njit
from scipy.stats import skewnorm


def calculate_diversity(batch_levels, batch_difficulties=None):
    differences = batch_levels.unsqueeze(-3) - batch_levels.unsqueeze(-2)
    differences = torch.linalg.norm(differences, dim=-1)

    if batch_difficulties is not None:
        weights = batch_difficulties.unsqueeze(-3) - batch_difficulties.unsqueeze(-2)
        weights = weights.squeeze(-1).abs()
    else:
        weights = 1

    return (weights * differences / 2).mean()


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
