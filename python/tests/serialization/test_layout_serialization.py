from unittest import TestCase

from NN.serialization import model_layout_to_bytes
from torch.nn import Sequential, Linear, Softmax, ReLU


class TestLayoutSerialization(TestCase):

    def test_serialization(self):
        model = Sequential(Linear(5, 6), Softmax(), Linear(6, 8), ReLU(), Linear(8, 1), ReLU(), Linear(1, 5), Softmax())
        bytes = model_layout_to_bytes(model)
        f = open('./layout.b', 'wb')
        f.write(bytes)
        f.close()
        print(len(bytes))
