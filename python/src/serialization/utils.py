from .general import DataTypes, Endianness


def get_format(data_type: DataTypes, endianness: Endianness, count: int) -> str:
    return f"{endianness}{count}{data_type}"
