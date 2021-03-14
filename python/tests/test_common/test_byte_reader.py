from unittest import TestCase

from common import ByteReader
from remote_computation.logging import LogOption
from serialization import to_bytes


class ByteReaderTest(TestCase):

    def test_bool(self):
        self.assertTrue(ByteReader(to_bytes(True)).read_bool())
        self.assertFalse(ByteReader(to_bytes(False)).read_bool())

    def test_log_option(self):
        option = LogOption.create(5, 100, True, True, True, 0.8)
        self.assertTrue(option.print)
        self.assertTrue(option.plot)
        self.assertTrue(option.min_max)
