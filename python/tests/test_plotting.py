import multiprocessing as mp
import time
from unittest import TestCase

import numpy as np


def update(queue: mp.Queue):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2)

    plt.ion()
    queue.put(None)
    print("[Child] Ready")

    for axis_id, data in iter(queue.get, None):
        print("received")
        ax[axis_id].plot(data)
        plt.draw()
        plt.pause(1)

    print("Done")


class PlottingTest(TestCase):
    def test_simple_plotting(self):
        import matplotlib.pyplot as plt

        # plt.ion()

        fig, ax = plt.subplots(2)

        ax[0].plot(np.random.normal(0, 1, 100))
        ax[1].plot(np.random.normal(0, 1, 100))

        plt.show()
        # plt.pause(0.001)

        # time.sleep(2)

    def test_update_from_another_thread(self):
        queue = mp.Queue()
        # plt.show()

        # plt.show(block=False)

        time.sleep(2)

        # plt.show()

        p = mp.Process(target=update, args=(queue,))
        p.start()

        queue.get()
        print("[Parent] Ready")

        queue.put((0, np.random.normal(0, 1, 100)))
        print("sent 1")
        time.sleep(2)
        queue.put((1, np.random.normal(0, 1, 100)))
        print("sent 2")
        time.sleep(2)
        queue.put(None)
        p.join()
