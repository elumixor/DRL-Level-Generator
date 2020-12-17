import time
from unittest import TestCase

from remote_computation import Communicator


class ServerTests(TestCase):

    def test_communicator(self):
        c = Communicator()
        self.assertFalse(c.is_running)
        c.start_update_loop()
        self.assertTrue(c.is_running)
        print("update loop started")
        time.sleep(1)
        self.assertTrue(c.is_running)
        print("update loop finishing")
        c.should_stop = True
        c.join()
        self.assertFalse(c.is_running)
        print("joined")

    # noinspection PyMethodMayBeStatic
    def test_just_start_for_ten_seconds(self):
        c = Communicator()
        c.start_update_loop()
        print("update loop started")
        time.sleep(10)
        c.join()

    # noinspection PyMethodMayBeStatic
    def test_start_server(self):
        c = Communicator()
        c.start_update_loop()
        c.join()
