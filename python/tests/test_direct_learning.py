import unittest

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F

from src.evaluators import DirectEvaluator
from src.utils import MLP
from .mlp_testing_utils import plot_intermediates, calculate_intermediates


class TestDirectLearning(unittest.TestCase):
    @unittest.skip("for visualization only")
    def test_basic_stuff(self):
        oracle = DirectEvaluator(0.3, np.deg2rad(50), 0.1, 0.1)

        x = np.linspace(-0.5, 0.5, 100)
        y = torch.from_numpy(oracle.evaluate(x)).type(torch.float32).unsqueeze(1)

        x = torch.from_numpy(x).unsqueeze(1).type(torch.float32)

        sizes = [2, 2]

        nn = MLP(1, 1, sizes, activation="lrelu")
        optim = torch.optim.Adam(nn.parameters(), lr=0.1)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optim, patience=100, factor=0.95, min_lr=0.001,
                                                               verbose=True)

        plt.ion()
        fig, axs = plt.subplots(max(sizes), len(sizes) + 2)
        plt.show(block=False)

        loss = float("inf")
        epoch = 0
        while loss > 1e-5:
            indices = torch.randperm(x.shape[0])[:10]

            loss = F.mse_loss(nn(x[indices]), y[indices])

            if epoch % 50 == 0:
                intermediates, last = calculate_intermediates(nn, sizes, x)
                plot_intermediates(axs, intermediates, last, x, y, clear=True)
                for ax in axs:
                    for a in ax:
                        a.set_xlim(-0.5, 0.5)
                        a.set_ylim(-0.25, 1)

                print(f"Epoch={epoch}. Loss={loss.item()}")

            epoch += 1

            optim.zero_grad()
            loss.backward()
            optim.step()
            scheduler.step(loss)

        print(f"Epoch={epoch}. Loss={loss.item()}")
        plot_intermediates(axs, intermediates, last, x, y)
        plt.show(block=True)
