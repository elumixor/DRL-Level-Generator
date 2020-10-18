import time
from unittest import TestCase

import serialization
from communication import Server, RequestType, ResponseType
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
        self.server.wait_for_stop()
        self.assertFalse(self.server.is_running)

    def test_server_echo(self):
        def handle_message(server, request_type, data):
            self.assertEqual(request_type, RequestType.Echo)

            string, length = serialization.to_string(data)

            self.assertEqual(string, "hello вёрльд")
            self.assertEqual(length, serialization.DataTypesSize.Int + len("hello вёрльд".encode('utf-8')))

            server.send_message(ResponseType.Echo, serialization.to_bytes(string))
            server.stop()

        self.server = Server(ADDRESS, handle_message)
        self.server.start()
        self.server.wait_for_stop()
