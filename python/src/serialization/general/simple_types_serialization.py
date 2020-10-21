from struct import pack, unpack
from typing import Callable, Tuple, Union, List, TypeVar

from . import SerializationException, ByteConvertible
from .data_types import DataTypes
from .data_types_size import DataTypesSize
from .endianness import Endianness
from ..utils import get_format


def int_to_bytes(value: int, endianness: Endianness = Endianness.Native) -> bytes:
    return pack(get_format(DataTypes.Int, endianness, 1), value)


def float_to_bytes(value: float, endianness: Endianness = Endianness.Native) -> bytes:
    return pack(get_format(DataTypes.Float, endianness, 1), value)


def string_to_bytes(value: str, endianness: Endianness = Endianness.Native) -> bytes:
    b = bytes(value, 'utf-8')
    return pack(get_format(DataTypes.Int, endianness, 1), len(b)) + b


def list_to_bytes(value: Union[List[int], List[float], List[str], List[ByteConvertible]],
                  endianness: Endianness = Endianness.Native) -> bytes:
    length = len(value)
    result = int_to_bytes(length, endianness)
    if length == 0:
        return result

    first = value[0]

    # more efficient conversions when using simple types
    if isinstance(first, int):
        result += pack(get_format(DataTypes.Int, endianness, length), *value)

        return result

    if isinstance(first, float):
        result += pack(get_format(DataTypes.Float, endianness, length), *value)

        return result

    if isinstance(first, str):
        for string in value:
            result += string_to_bytes(string, endianness)

        return result

    # general list conversions
    if isinstance(first, ByteConvertible):
        for convertible in value:
            result += convertible.to_bytes(endianness)

        return result

    raise SerializationException(f"Cannot convert list of type {type(value)} to bytes")


def to_int(value: bytes, start_index: int = 0, endianness: Endianness = Endianness.Native) -> int:
    fmt = get_format(DataTypes.Int, endianness, 1)
    return unpack(fmt, value[start_index: start_index + DataTypesSize.Int])[0]


def to_float(value: bytes, start_index: int = 0, endianness: Endianness = Endianness.Native) -> float:
    fmt = get_format(DataTypes.Float, endianness, 1)
    return unpack(fmt, value[start_index: start_index + DataTypesSize.Float])[0]


def to_string(value: bytes, start_index: int = 0, endianness: Endianness = Endianness.Native) -> Tuple[str, int]:
    length = to_int(value, start_index, endianness)
    value = value[start_index + DataTypesSize.Int:start_index + DataTypesSize.Int + length]
    string = value.decode('utf-8')
    return string, DataTypesSize.Int + length


T = TypeVar('T')


def to_list(value: bytes, transformer: Callable[[bytes, int, Endianness], Tuple[T, int]], start_index: int = 0,
            endianness: Endianness = Endianness.Native) -> Tuple[List[T], int]:
    length = unpack(get_format(DataTypes.Int, endianness, 1), value[start_index: start_index + DataTypesSize.Int])[0]
    result = []
    start_index += DataTypesSize.Int
    total_read_bytes = 0
    for _ in range(length):
        item, read_bytes = transformer(value, start_index + total_read_bytes, endianness)
        result.append(item)
        total_read_bytes += read_bytes

    return result, total_read_bytes + DataTypesSize.Int


def to_list_int(value: bytes, start_index: int = 0, endianness: Endianness = Endianness.Native) -> Tuple[List[int], int]:
    length = unpack(get_format(DataTypes.Int, endianness, 1), value[start_index: start_index + DataTypesSize.Int])[0]
    start_index += DataTypesSize.Int
    total_read_bytes = length * DataTypesSize.Int

    result = list(unpack(get_format(DataTypes.Int, endianness, length), value[start_index: start_index + total_read_bytes]))
    return result, total_read_bytes + DataTypesSize.Int


def to_list_float(value: bytes, start_index: int = 0, endianness: Endianness = Endianness.Native) -> Tuple[List[float], int]:
    length = unpack(get_format(DataTypes.Int, endianness, 1), value[start_index: start_index + DataTypesSize.Int])[0]
    start_index += DataTypesSize.Int
    total_read_bytes = length * DataTypesSize.Float

    result = list(unpack(get_format(DataTypes.Float, endianness, length), value[start_index: start_index + total_read_bytes]))
    return result, total_read_bytes + DataTypesSize.Int


def to_list_int_fixed(value: bytes, length: int, start_index: int = 0, endianness: Endianness = Endianness.Native) -> Tuple[List[int], int]:
    total_read_bytes = length * DataTypesSize.Int

    result = list(unpack(get_format(DataTypes.Int, endianness, length), value[start_index: start_index + total_read_bytes]))
    return result, total_read_bytes


def to_list_float_fixed(value: bytes, length: float, start_index: int = 0, endianness: Endianness = Endianness.Native) -> Tuple[
    List[int], int]:
    total_read_bytes = length * DataTypesSize.Float

    result = list(unpack(get_format(DataTypes.Float, endianness, length), value[start_index: start_index + total_read_bytes]))
    return result, total_read_bytes


def to_list_strings(value: bytes, start_index: int = 0, endianness: Endianness = Endianness.Native) -> Tuple[List[str], int]:
    return to_list(value, to_string, start_index, endianness)
