from collections import OrderedDict
from typing import Union

import torch

from .byte_assignable import ByteAssignable
from .byte_convertible import ByteConvertible
from .byte_serializable import ByteSerializable
from .data_types import DataTypes
from .data_types_size import DataTypesSize
from .endianness import Endianness
from .serialization_exception import SerializationException
from .simple_types_serialization import int_to_bytes, float_to_bytes, string_to_bytes, to_string, to_float, to_int, to_list, list_to_bytes, \
    to_list_float, to_list_strings, to_list_int, to_list_float_fixed, to_list_int_fixed

Serializable = Union[int, float, str, ByteConvertible, OrderedDict, torch.Tensor]
