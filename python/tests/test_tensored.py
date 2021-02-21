import torch

from base_test import BaseTest
from common import tensored


@tensored
class TestInstance(torch.Tensor):
    def __init__(self, attr0, attr1):
        pass


class TestTensored(BaseTest):
    def test_inheritance(self):
        instance = TestInstance(0, 1)
        self.assertIsInstance(instance, torch.Tensor)

    def test_access(self):
        instance = TestInstance(0, 1)
        self.assertHasAttr(instance, "attr0")
        self.assertHasAttr(instance, "attr1")

    def test_values(self):
        instance = TestInstance(0, 1)
        self.assertAlmostEqual(instance.attr0, 0)
        self.assertAlmostEqual(instance.attr1, 1)

    def test_does_not_modify_tensor_class(self):
        _ = TestInstance(0, 1)
        another = torch.tensor([1, 2, 3])
        self.assertNotHasAttr(another, "attr0")

    def test_default_tensor_operations(self):
        instance = TestInstance(0, 1)
        instance = instance + instance * 2
        self.assertAlmostEqual(instance[0], 0)
        self.assertAlmostEqual(instance[1], 3)
