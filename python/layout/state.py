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


def bytes2state(bytes):
    return torch.tensor(struct.unpack(f'>{state_size}f', *bytes), dtype=torch.float)


def bytes2training_data(bytes):
    # training data is stored in form
