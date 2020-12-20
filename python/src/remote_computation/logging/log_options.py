from common import ByteReader
from .log_option import LogOption
from .log_option_name import LogOptionName


class LogOptions(dict):

    def __init__(self, reader: ByteReader):
        super().__init__()
        self.length = reader.read_int()
        self[LogOptionName(reader.read_int())] = LogOption(reader)
