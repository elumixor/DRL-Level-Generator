import multiprocessing as mp
import os
import signal
import time
from unittest import TestCase


def dummy():
    # def on_signal(signum, stack):
    #     print(f"received {signum}")
    #     print(stack)

    # signal.signal(signal.SIGFPE, on_signal)

    print("hello")
    time.sleep(2)

    print("done")

    # signal.sigwait()


class ProcessesTests(TestCase):

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
