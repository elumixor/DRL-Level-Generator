from collections import OrderedDict
from typing import Union, List

import torch

from .byte_assignable import ByteAssignable
from .byte_convertible import ByteConvertible
from .byte_serializable import ByteSerializable
from .data_types import DataTypes
from .data_types_size import DataTypesSize
from .endianness import Endianness
from .serialization_exception import SerializationException
from .simple_types_serialization import int_to_bytes, float_to_bytes, string_to_bytes, to_string, to_float, to_int, to_list, list_to_bytes, \
    to_float_list, to_string_list, to_int_list
from .torch_serialization import to_bytes as state_dict_to_bytes, to_state_dict, tensor_to_bytes, to_tensor_int, to_tensor_float
from .utils import __get_format

Serializable = Union[int, float, str, ByteConvertible, OrderedDict, torch.Tensor]


def to_bytes(value: Union[Serializable, List[int], List[float], List[str], List[ByteConvertible]],
             endianness: Endianness = Endianness.Native) -> bytes:
    """
    Converts a given object to bytes
    :param value: Object to be converted
    :param endianness: Endianness to be used
    :return:
    """
    if isinstance(value, ByteConvertible):
        return value.to_bytes(endianness)

    if isinstance(value, torch.Tensor):
        return tensor_to_bytes(value, endianness)

    if isinstance(value, OrderedDict):
        return state_dict_to_bytes(value, endianness)

    if isinstance(value, List):
        return list_to_bytes(value, endianness)

    if isinstance(value, int):
        return int_to_bytes(value, endianness)

    if isinstance(value, float):
        return float_to_bytes(value, endianness)

    if isinstance(value, str):
        return string_to_bytes(value, endianness)

    raise SerializationException(f"Cannot type {type(value)} to bytes")
