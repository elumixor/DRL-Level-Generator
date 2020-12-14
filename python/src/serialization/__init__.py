from typing import List

from torch.nn import Sequential

from .general import *
from .torch_serialization import tensor_to_bytes, state_dict_to_bytes, to_tensor_int, to_tensor_float, to_state_dict, layout_to_bytes
from .training_data_serialization import to_training_data
from .utils import get_format


def to_bytes(value: Union[Serializable, List[int], List[float], List[str], List[ByteConvertible], Sequential],
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

    if isinstance(value, Sequential):
        return layout_to_bytes(value)

    raise RuntimeError(f"Cannot type {type(value)} to bytes")
