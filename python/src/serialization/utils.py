from .data_types import DataTypes
from .endianness import Endianness


def __get_format(data_type: DataTypes, endianness: Endianness, count: int) -> str:
    return f"{endianness}{count}{data_type}"
