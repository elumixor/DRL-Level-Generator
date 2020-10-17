from struct import pack, unpack
from typing import Union, List, Callable, Tuple

from .byte_assignable import ByteAssignable
from .byte_convertible import ByteConvertible
from .byte_serializable import ByteSerializable
from .data_types import DataTypes
from .data_types_size import DataTypesSize
from .endianness import Endianness


def __get_format(data_type: DataTypes, endianness: Endianness, count: int) -> str:
    return f"{endianness.value}{count}{data_type.value}"


def to_bytes(value: Union[int, float, str, ByteConvertible, List[int], List[float], List[str], List[ByteConvertible]],
             endianness: Endianness = Endianness.Native) -> bytes:
    """
    Converts a given object to bytes
    :param value: Object to be converted
    :param endianness: Endianness to be used
    :return:
    """
    if isinstance(value, ByteConvertible):
        return bytes(value)

    if isinstance(value, List):
        result = pack(__get_format(DataTypes.Int, endianness, 1), len(value))
        if len(value) == 0:
            return result

        first = value[0]
        if isinstance(first, ByteConvertible):
            for convertible in value:
                result += bytes(convertible)

            return result

        if isinstance(first, int):
            result += pack(__get_format(DataTypes.Int, endianness, len(value)), *value)

            return result

        if isinstance(first, float):
            result += pack(__get_format(DataTypes.Float, endianness, len(value)), *value)

            return result

        if isinstance(first, str):
            for string in value:
                result += to_bytes(string)

            return result

        raise Exception(f"Cannot convert list of type {type(value)} to bytes")

    if isinstance(value, int):
        return pack(__get_format(DataTypes.Int, endianness, 1), value)

    if isinstance(value, float):
        return pack(__get_format(DataTypes.Float, endianness, 1), value)

    if isinstance(value, str):
        return pack(__get_format(DataTypes.Int, endianness, 1), len(value)) + bytes(value, 'ascii')

    raise Exception(f"Cannot type {type(value)} to bytes")


def to_int(value: bytes, start_index: int = 0, endianness: Endianness = Endianness.Native) -> int:
    fmt = __get_format(DataTypes.Int, endianness, 1)
    return unpack(fmt, value[start_index: start_index + DataTypesSize.Int.value])[0]


def to_float(value: bytes, start_index: int = 0, endianness: Endianness = Endianness.Native) -> float:
    fmt = __get_format(DataTypes.Float, endianness, 1)
    return unpack(fmt, value[start_index: start_index + DataTypesSize.Float.value])[0]


def to_string(value: bytes, start_index: int = 0, endianness: Endianness = Endianness.Native) -> Tuple[str, int]:
    length = to_int(value, start_index, endianness)
    value = value[start_index + DataTypesSize.Int.value:start_index + DataTypesSize.Int.value + length * DataTypesSize.Char.value]
    string = value.decode('ascii')
    return string, DataTypesSize.Int.value + len(string) * DataTypesSize.Char.value


def to_list(value: bytes, transformer: Callable, start_index: int = 0, endianness: Endianness = Endianness.Native):
    length = unpack(__get_format(DataTypes.Int, endianness, 1), value[start_index: start_index + DataTypesSize.Int.value])[0]
    result = []
    start_index = start_index + DataTypesSize.Int.value
    total_read_bytes = 0
    for _ in range(length):
        item, read_bytes = transformer(value, start_index + total_read_bytes, endianness)
        result.append(item)
        total_read_bytes += read_bytes

    return result, total_read_bytes
