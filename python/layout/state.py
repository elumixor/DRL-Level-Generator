import struct
import torch

# state contains:
# - positions of the enemies (2) * 3 = (6)
# - position of the player (handle) (1)
# - current angle (1)
# - current angular speed (1)
# - current upward speed (1)
# 6 + 1 + 1 + 1 + 1 = 10 floats
state_size = 10

# training data is stored in form of
# - length n
# - previous states (10)
# - selected action (1)
# - rewards (1)
# - next states (10)
# 23 * n floats
transition_size = 2 * state_size + 1 + 1


def bytes2state(b):
    return torch.tensor(struct.unpack(f'{state_size}f', b), dtype=torch.float)


def bytes2training_data(b, offset=0):
    length = struct.unpack('i', b[offset:offset + 4])[0]
    offset += 4

    episodes = []

    for i in range(length):
        episode = bytes2episode(b, offset)
        episode_length = episode[0].shape[0]

        offset += 4 + episode_length * transition_size * 4
        episodes.append(episode)

    rewards = [e[2].sum() for e in episodes]
    print(torch.tensor(rewards).mean())

    return episodes


def bytes2episode(b, offset=0):
    length = struct.unpack('i', b[offset:offset + 4])[0]
    offset += 4

    data = struct.unpack(f'{transition_size * length}f',
                         b[offset:offset + length * transition_size * 4])

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

    return states, selected_actions, rewards, next_states
