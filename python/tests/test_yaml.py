import os
from unittest import TestCase

from common import read_yaml


class Test(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open("config.yaml", "w") as f:
            f.write("entry:\n  value: 1")

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("config.yaml")

    def test_open_yaml(self):
        with read_yaml("config") as y:
            self.assertEqual(y.entry.value, 1)

        with read_yaml("config.yaml") as y:
            self.assertEqual(y.entry.value, 1)
