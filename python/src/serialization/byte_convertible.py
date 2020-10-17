from abc import abstractmethod


class ByteConvertible:
    """
    Converts itself to byte array
    """

    @abstractmethod
    def __bytes__(self) -> bytes:
        """
        Converts itself to byte array
        :return: Bytes of this data
        """
        pass
