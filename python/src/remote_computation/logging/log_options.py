from typing import List, Tuple

from common import ByteReader
from serialization import to_bytes
from .log_option import LogOption
from .log_option_name import LogOptionName


class LogOptions(dict):

    def __init__(self, reader: ByteReader):
        super().__init__()
        self.length = reader.read_int()

        for _ in range(self.length):
            opt = reader.read_int()
            self[LogOptionName(opt)] = LogOption(reader)

    def to_bytes(self) -> bytes:
        b = to_bytes(self.length)

        for key, value in self:
            key: LogOptionName
            value: LogOption

            b += to_bytes(key)
            b += value.to_bytes()

        return b

    @staticmethod
    def create(options: List[Tuple[LogOptionName, LogOption]]):
        result = LogOptions(ByteReader(to_bytes(0)))

        result.length = len(options)

        for option_name, option in options:
            result[option_name] = option

        return result
