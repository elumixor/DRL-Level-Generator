import multiprocessing as mp
import os
import signal
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from unittest import TestCase

from remote_computation import Communicator


def dummy():
    # def on_signal(signum, stack):
    #     print(f"received {signum}")
    #     print(stack)

    # signal.signal(signal.SIGFPE, on_signal)

    print("hello")
    time.sleep(2)

    print("done")

    # signal.sigwait()


_my_signal = 1


def my_process(queue):
    print(_my_signal)
    for value in iter(queue.get, None):
        print(f"received {value}")

    print("received sentinel, ending...")


class ParallelismTests(TestCase):

    def test_pid(self):
        p = mp.Process(target=dummy)
        p.start()
        self.assertIsNotNone(p.pid)
        self.assertTrue(p.is_alive())
        print(p.name)
        time.sleep(1)
        os.kill(p.pid, signal.SIGFPE)
        # p.join()
        # self.assertFalse(p.is_alive())
        time.sleep(1)

    def test_multithreading_with_communicator(self):
        c = Communicator()
        print(c)

        def t():
            print(f"thread {c}")

        t = threading.Thread(target=t)
        t.start()

        t.join()

    def test_executor(self):
        executor = ThreadPoolExecutor()

        def pow(a, b):
            time.sleep(1)
            return a ** b

        result = executor.submit(pow, 2, 2)

        self.assertTrue(result.running())
        self.assertEqual(4, result.result())  # note: blocks
        self.assertFalse(result.running())

    def test_process_waiting_for_data(self):
        q = mp.Queue()

        p = mp.Process(target=my_process, args=(q,))
        p.start()

        q.put("hello")
        time.sleep(2)
        q.put(None)

        p.join()
