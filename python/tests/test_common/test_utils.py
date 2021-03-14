from unittest import TestCase

import torch

from core.analysis import timed
from core.utils import bootstrap


# noinspection PyTypeChecker
class UtilsTests(TestCase):

    def test_bootstrapping(self):
        r = torch.tensor([1, 1, 2, 2, 1], dtype=torch.float32)
        V_next = torch.tensor([1, 2, 3, 4, 5], dtype=torch.float32)
        gamma = 0.99

        with timed():
            for _ in range(10000):
                Gt = bootstrap(r, V_next, 3, gamma)

        self.assertAlmostEqual(Gt[0].item(), (r[0] + gamma * r[1] + gamma ** 2 * r[2] + gamma ** 3 * V_next[2]).item())
        self.assertAlmostEqual(Gt[1].item(), (r[1] + gamma * r[2] + gamma ** 2 * r[3] + gamma ** 3 * V_next[3]).item())
        self.assertAlmostEqual(Gt[2].item(), (r[2] + gamma * r[3] + gamma ** 2 * r[4] + gamma ** 3 * V_next[4]).item())
        self.assertAlmostEqual(Gt[3].item(), (r[3] + gamma * r[4] + gamma ** 2 * V_next[4]).item())
        self.assertAlmostEqual(Gt[4].item(), (r[4] + gamma * V_next[4]).item())

        r = torch.tensor([1, 1, 2], dtype=torch.float32)
        V_next = torch.tensor([1, 2, 3], dtype=torch.float32)

        with timed():
            for _ in range(10000):
                Gt = bootstrap(r, V_next, 3, gamma)

        self.assertAlmostEqual(Gt[0].item(), (r[0] + gamma * r[1] + gamma ** 2 * r[2] + gamma ** 3 * V_next[2]).item())
        self.assertAlmostEqual(Gt[1].item(), (r[1] + gamma * r[2] + gamma ** 2 * V_next[2]).item())
        self.assertAlmostEqual(Gt[2].item(), (r[2] + gamma * V_next[2]).item())

        r = torch.tensor([1, 2], dtype=torch.float32)
        V_next = torch.tensor([1, 3], dtype=torch.float32)

        with timed():
            for _ in range(10000):
                Gt = bootstrap(r, V_next, 3, gamma)

        self.assertAlmostEqual(Gt[0].item(), (r[0] + gamma * r[1] + gamma ** 2 * V_next[1]).item())
        self.assertAlmostEqual(Gt[1].item(), (r[1] + gamma * V_next[1]).item())
