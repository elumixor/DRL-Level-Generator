# state contains:
# - positions of the enemies (2) * 3 = (6)
# - position of the player (handle) (1)
# - current angle (1)
# - current angular speed (1)
# - current upward speed (1)
# 6 + 1 + 1 + 1 + 1 = 10 floats
import struct

import torch

state_size = 10


def bytes2state(b):
    return torch.tensor(struct.unpack(f'{state_size}f', b), dtype=torch.float)


def bytes2training_data(b):
    # training data is stored in form of
    # - length n
    # - previous states (10)
    # - selected action (1)
    # - rewards (1)
    # - next states (10)
    # 23 * n floats
    transition_size = 2 * state_size + 1 + 1

    length = struct.unpack('i', b[0:4])[0]

    data = struct.unpack(f'{transition_size * length}f',
                         b[4:4 + length * transition_size * 4])

    def data_slice(size, stride, i):
        return slice(transition_size * i + stride, transition_size * i + size + stride)

    length_range = range(length)

    states = torch.tensor([data[data_slice(state_size, 0, i)] for i in length_range],
                          dtype=torch.float, device='cuda')
    selected_actions = torch.tensor([data[data_slice(1, state_size, i)] for i in length_range],
                                    dtype=torch.long, device='cuda')
    rewards = torch.tensor([data[data_slice(1, state_size + 1, i)] for i in length_range],
                           dtype=torch.float, device='cuda')
    next_states = torch.tensor([data[data_slice(state_size, state_size + 1 + 1, i)] for i in length_range],
                               dtype=torch.float, device='cuda')

    print(f"Total reward: {rewards.sum().cpu().item()}")

    return states, selected_actions, rewards, next_states
