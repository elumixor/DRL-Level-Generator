from common import ByteReader


class LogOption:

    def __init__(self, reader: ByteReader):
        self.frequency = reader.read_int()
        self.logLastN = reader.read_int()
        self.print = reader.read_bool()
        self.plot = reader.read_bool()
        self.minMax = reader.read_bool()
        self.runningAverageSmoothing = reader.read_float()
