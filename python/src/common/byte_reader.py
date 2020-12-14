import struct
from collections import OrderedDict
from typing import List

import torch


class ByteReader:

    def __init__(self, b: bytes, start_index: int = 0):
        self.b = b
        self.current_index = start_index

    def read_int(self):
        return struct.unpack('i', self._get_part(4))[0]

    def read_float(self):
        return struct.unpack('f', self._get_part(4))[0]

    def read_string(self):
        length = self.read_int()
        value = self._get_part(length)
        string = value.decode('utf-8')
        return string

    def read_to_end(self):
        result = self.b[self.current_index:]
        self.current_index = len(self.b)
        return result

    def _get_part(self, size):
        result = self.b[self.current_index:self.current_index + size]
        self.current_index += size
        return result

    def read_list_int(self) -> List[int]:
        length = self.read_int()

        result = list(struct.unpack(f"{length}i", self._get_part(length * 4)))
        return result

    def read_list_float(self) -> List[float]:
        length = self.read_int()

        result = list(struct.unpack(f"{length}f", self._get_part(length * 4)))
        return result

    def read_float_tensor(self):
        shape = self.read_list_int()

        items = self.read_list_float()

        return torch.tensor(items).reshape(shape)

    def read_state_dict(self):
        entries_length = self.read_int()

        d = OrderedDict()

        for i in range(entries_length):
            key = self.read_string()
            tensor = self.read_float_tensor()
            d[key] = tensor

        return d

    def read_transition(self):
        state = self.read_list_float()
        action = self.read_list_float()
        reward = self.read_float()
        next_state = self.read_list_float()
        return state, action, reward, next_state

    def read_trajectory(self):
        trajectory_length = self.read_int()
        trajectory = []

        for _ in range(trajectory_length):
            transition = self.read_transition()
            trajectory.append(transition)

        return trajectory
