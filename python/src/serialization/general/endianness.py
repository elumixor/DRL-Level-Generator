from enum import Enum


class Endianness(str, Enum):
    Native = '='
    Big = '>'
    Little = '<'
