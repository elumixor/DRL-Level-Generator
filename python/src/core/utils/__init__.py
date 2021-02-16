import torch

from .auto_eval import auto_eval
from .epsilon_decay import EpsilonDecay
from .mlp import mlp as MLP


# @lru_cache(maxsize=128, typed=False)
def get_gammas_for(n, discounting):
    gammas = torch.ones([n + 1], dtype=torch.float32)
    current = discounting
    for i in range(1, n + 1):
        gammas[i] = current
        current *= discounting

    return gammas


def bootstrap(rewards, values_next, n, discounting):
    results = torch.zeros_like(rewards)
    T = results.shape[0]

    for t in range(T - n):
        results[t] = rewards[t]
        for i in range(1, n):
            results[t] = results[t] + (discounting ** i) * rewards[t + i]

        results[t] = (discounting ** n) * values_next[t + n - 1]

    for t in range(T - n, T):
        results[t] = rewards[t]

        for i in range(1, T - t):
            results[t] = results[t] + (discounting ** i) * rewards[t + i]

    return results


def bootstrap2(rewards, values_next, n, discounting):
    gammas = get_gammas_for(n, discounting)
    T = rewards.shape[0]
    results = torch.zeros([T])

    for t in range(T):
        last = min(T - t, n)
        g = gammas[:last]

        end = min(t + n, T)
        results[t] = (g * rewards[t: end]).sum() + gammas[end - t] * values_next[end - 1]

    return results


def bootstrap3(rewards, values_next, n, discounting):
    gammas = get_gammas_for(n, discounting)
    T = rewards.shape[0]
    results = torch.zeros([T])

    last_gamma = gammas[n]
    for t in range(T - n + 1):
        g = gammas[:-1]

        results[t] = (g * rewards[t: t + n]).sum() + last_gamma * values_next[t + n - 1]

    for t in range(max(0, T - n + 1), T):
        last = min(T - t, n)
        g = gammas[:last]

        end = min(t + n, T)
        results[t] = (g * rewards[t: end]).sum() + gammas[end - t] * values_next[end - 1]

    return results


def discounted_rewards(rewards, discounting):
    res = torch.zeros_like(rewards)
    last = 0.0
    for i in reversed(range(rewards.shape[0])):
        last = res[i] = rewards[i] + discounting * last

    return res


def map_transitions(transitions):
    states, actions, rewards, done, next_states = zip(*transitions)

    states = torch.stack(states).detach()
    actions = torch.stack(actions).detach()
    rewards = torch.tensor(rewards).detach()
    done = torch.tensor(done)
    next_states = torch.stack(next_states).detach()

    return states, actions, rewards, done, next_states
