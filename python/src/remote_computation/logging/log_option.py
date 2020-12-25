from common import ByteReader
from serialization import to_bytes


class LogOption:

    def __init__(self, reader: ByteReader):
        self.frequency = reader.read_int()
        self.log_last_n = reader.read_int()
        self.print = reader.read_bool()
        self.plot = reader.read_bool()
        self.min_max = reader.read_bool()
        self.running_average_smoothing = reader.read_float()

    def to_bytes(self) -> bytes:
        b = b''
        b += to_bytes(self.frequency)
        b += to_bytes(self.log_last_n)
        b += to_bytes(self.print)
        b += to_bytes(self.plot)
        b += to_bytes(self.min_max)
        b += to_bytes(self.running_average_smoothing)
        return b

    @staticmethod
    def create(frequency, log_last_n, print, plot, min_max, running_average_smoothing):
        b = b''

        b += to_bytes(frequency)
        b += to_bytes(log_last_n)
        b += to_bytes(print)
        b += to_bytes(plot)
        b += to_bytes(min_max)
        b += to_bytes(running_average_smoothing)

        return LogOption(ByteReader(b))
