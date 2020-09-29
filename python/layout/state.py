# state contains:
# - positions of the enemies (2) * 3 = (6)
# - position of the player (handle) (1)
# - current angle (1)
# - current angular speed (1)
# - current upward speed (1)
# total: 6 + 1 + 1 + 1 + 1 = 10
import struct

import torch

state_size = 10


def bytes2state(b):
    return torch.tensor(struct.unpack(f'>{state_size}f', b), dtype=torch.float)


def bytes2training_data(b):
    # training data is stored in form of
    # - length n
    # - states [n] (10 floats)
    # - actions [n] (single float)
    # - rewards [n] (single float)
    length = struct.unpack('>i', b[0:4])[0]

    state_bytes = 4 * state_size * length
    actions_bytes = 4 * length
    rewards_bytes = 4 * length

    states = struct.unpack(f'>{state_size * length}f', b[4:4 + state_bytes])
    actions = struct.unpack(f'>{state_size * length}f', b[4 + state_bytes: 4 + state_bytes + actions_bytes])
    rewards = struct.unpack(f'>{state_size * length}f',
                            b[4 + state_bytes + actions_bytes:4 + state_bytes + actions_bytes + rewards_bytes])

    return (states, actions, rewards)
