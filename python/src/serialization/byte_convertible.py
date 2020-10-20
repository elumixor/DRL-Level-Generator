from abc import abstractmethod

from .endianness import Endianness


class ByteConvertible:
    """
    Converts itself to byte array
    """

    @abstractmethod
    def to_bytes(self, endianness: Endianness = Endianness.Native) -> bytes:
        """
        Converts itself to byte array
        :return: Bytes of this data
        """
        pass
