from abc import abstractmethod

from .byte_assignable import ByteAssignable
from .byte_convertible import ByteConvertible
from .endianness import Endianness


class ByteSerializable(ByteConvertible, ByteAssignable):
    @abstractmethod
    def assign_from_bytes(self, bytes_value: bytes, start_index: int = 0, endianness: Endianness = Endianness.Native) -> int:
        pass

    @abstractmethod
    def __bytes__(self) -> bytes:
        pass
