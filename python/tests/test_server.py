import time
from unittest import TestCase

from communication import Server
from communication.server_exception import ServerException

ADDRESS = "tcp://*:5555"


class ServerTests(TestCase):
    def setUp(self) -> None:
        self.server = Server(ADDRESS, None)

    def tearDown(self) -> None:
        if self.server is not None:
            self.server.stop()

    def test_can_start_server(self):
        self.assertFalse(self.server.is_running)
        self.server.start()
        self.assertTrue(self.server.is_running)

    def test_cannot_start_twice(self):
        self.server.start()
        self.assertTrue(self.server.is_running)
        self.assertRaises(ServerException, lambda: self.server.start())

    def test_server_is_non_blocking(self):
        self.assertFalse(self.server.is_running)
        self.server.start()
        time.sleep(0.1)
        self.assertTrue(self.server.is_running)
        self.server.stop()
        time.sleep(0.1)
        self.assertFalse(self.server.is_running)
