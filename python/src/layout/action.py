import struct

# action is just a single number
action_size = 2


def action2bytes(action):
    return struct.pack('f', 1 if action.item() > 0 else 0)
