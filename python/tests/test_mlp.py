from unittest import TestCase

from src.utils import MLP


class TestMLP(TestCase):
    def test_import(self):
        nn = MLP(1, 2, [3, 4])
        self.assertIsNotNone(nn)
