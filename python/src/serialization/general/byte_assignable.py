from abc import abstractmethod

from .endianness import Endianness


class ByteAssignable:
    @abstractmethod
    def assign_from_bytes(self, bytes_value: bytes, start_index: int = 0, endianness: Endianness = Endianness.Native) -> int:
        """
        Assigns self values from bytes
        :param bytes_value: Bytes to assign from
        :param start_index: Offset of data
        :param endianness: Endianness to be used
        :return: Number of read bytes
        """
        pass
