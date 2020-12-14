import random
import time
from multiprocessing import Queue
from unittest import TestCase

from remote_computation.communicator import Communicator


def worker(a1, queue: Queue):
    print(f"Worker {a1}")
    time.sleep(random.random())
    print(f"Worker {a1} finished")
    queue.put(a1)


class TestCommunicator(TestCase):

    def test_update_loop(self):
        communicator = Communicator(5671, 5672)
        communicator.start_update_loop()

        time.sleep(1)

        communicator.join()
