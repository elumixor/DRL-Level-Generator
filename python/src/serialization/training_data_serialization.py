from typing import List, Tuple

import torch

from DRL import Episode
from .general import to_list, to_list_float_fixed, DataTypesSize, to_int


def get_episode_flat(state_size, action_size):
    transition_size = 2 * state_size + action_size + 1

    def transformer(data, start, _):
        episode_length = to_int(data, start)
        start += DataTypesSize.Int
        num_floats = episode_length * transition_size
        value, bytes_read = to_list_float_fixed(data, num_floats, start)
        return value, bytes_read + DataTypesSize.Int

    return transformer


def episode_to_tensors(episode: List[float], state_size, action_size, device):
    transition_size = 2 * state_size + action_size + 1

    def data_slice(size, stride, i):
        return slice(transition_size * i + stride, transition_size * i + size + stride)

    length_range = range(int(len(episode) / transition_size))
    stride = 0

    states = [episode[data_slice(state_size, stride, i)] for i in length_range]
    stride += state_size

    actions = [episode[data_slice(action_size, stride, i)] for i in length_range]
    stride += action_size

    rewards = [episode[data_slice(1, stride, i)] for i in length_range]
    stride += 1

    next_states = [episode[data_slice(state_size, stride, i)] for i in length_range]

    states = torch.tensor(states, dtype=torch.float32, device=device)
    next_states = torch.tensor(next_states, dtype=torch.float32, device=device)
    actions = torch.tensor(actions, dtype=torch.float32, device=device).long()
    rewards = torch.tensor(rewards, dtype=torch.float32, device=device)

    return states, actions, rewards, next_states


def to_training_data(training_data_bytes: bytes, start_index: int, state_size: int, action_size: int, device='cuda') -> \
        Tuple[List[Episode], int]:
    training_data, bytes_read = to_list(training_data_bytes, get_episode_flat(state_size, action_size), start_index)
    training_data = [episode_to_tensors(episode, state_size, action_size, device) for episode in training_data]
    return training_data, bytes_read
