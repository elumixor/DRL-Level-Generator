from collections import OrderedDict
from enum import Enum
from typing import Tuple

import torch
from torch.nn import Sequential, Linear, Softmax, ReLU

from .general import Endianness, DataTypesSize, int_to_bytes, string_to_bytes, list_to_bytes, to_int, to_string, to_list_int, to_list_float


def state_dict_to_bytes(state_dict: OrderedDict, endianness: Endianness = Endianness.Native):
    result = int_to_bytes(len(state_dict), endianness)
    for key in state_dict:
        result += string_to_bytes(key, endianness)
        result += tensor_to_bytes(state_dict[key], endianness)
    return result


def to_state_dict(value: bytes, start_index: int = 0, endianness: Endianness = Endianness.Native) -> Tuple[OrderedDict, int]:
    entries_length = to_int(value, start_index, endianness)
    total_read = DataTypesSize.Int

    d = OrderedDict()
    for i in range(entries_length):
        key, read_bytes = to_string(value, start_index + total_read, endianness)
        total_read += read_bytes
        tensor, read_bytes = to_tensor_float(value, start_index + total_read, endianness)
        total_read += read_bytes
        d[key] = tensor

    return d, total_read


def tensor_to_bytes(tensor_value: torch.Tensor, endianness: Endianness = Endianness.Native) -> bytes:
    return list_to_bytes(list(tensor_value.shape), endianness) + list_to_bytes(tensor_value.flatten().tolist(), endianness)


def to_tensor_float(value: bytes, start_index: int = 0, endianness: Endianness = Endianness.Native) -> Tuple[torch.Tensor, int]:
    shape, bytes_read = to_list_int(value, start_index, endianness)
    total_read = bytes_read

    items, bytes_read = to_list_float(value, start_index + total_read, endianness)
    total_read += bytes_read

    return torch.tensor(items).reshape(shape), total_read


def to_tensor_int(value: bytes, start_index: int = 0, endianness: Endianness = Endianness.Native) -> Tuple[torch.Tensor, int]:
    shape, bytes_read = to_list_int(value, start_index, endianness)
    total_read = bytes_read

    items, bytes_read = to_list_int(value, start_index + total_read, endianness)
    total_read += bytes_read

    return torch.tensor(items).reshape(shape), total_read


class LayerName(int, Enum):
    Linear = 0
    ReLU = 1
    Softmax = 2
    Sequential = 3


def layout_to_bytes(model: Sequential):
    if not isinstance(model, Sequential):
        raise RuntimeError("Works only with Sequential models")

    result = int_to_bytes(len(model))

    for child in model.children():
        if isinstance(child, Linear):
            result += int_to_bytes(LayerName.Linear)
            result += int_to_bytes(child.in_features)
            result += int_to_bytes(child.out_features)
        elif isinstance(child, Softmax):
            result += int_to_bytes(LayerName.Softmax)
        elif isinstance(child, ReLU):
            result += int_to_bytes(LayerName.ReLU)
        else:
            raise RuntimeError(f"Layer is not supported yet: {type(child)}")

    return result
