import unittest

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F

from src.utils import MLP


class TestMLP(unittest.TestCase):
    def test_basic_stuff(self):
        nn = MLP(1, 2, [3, 4])
        self.assertIsNotNone(nn)

        self.assert_activation_is_relu(nn.activation)

        x = torch.tensor([[1.0]])
        self.assertEqual(nn(x).shape, torch.Size([1, 2]))

    def assert_activation_is_relu(self, activation: torch.nn.Module):
        x = torch.tensor([-1, 0, 1], dtype=torch.float32)
        y = activation(x)

        self.assertTrue(torch.all(y == torch.tensor([0, 0, 1], dtype=torch.float32)))

    @unittest.skip("for visualization only")
    def test_learning_linear_function(self):
        for _ in range(10):
            x = torch.linspace(-1, 1, 100).reshape(-1, 1)
            y = x

            nn = MLP(1, 1)
            optim = torch.optim.Adam(nn.parameters(), lr=0.1)

            previous_loss = float("inf")

            for _ in range(100000):
                predicted = nn(x)
                loss = F.mse_loss(y, predicted)

                # self.assertLess(loss.item(), previous_loss)

                optim.zero_grad()
                loss.backward()
                optim.step()

                previous_loss = loss.item()

            self.assertLess(previous_loss, 1e-5)

        print("ok")

    @unittest.skip("for visualization only")
    def test_visualization(self):
        print(torch.seed())
        plt.ion()
        fig, axs = plt.subplots(2, 3)
        plt.show(block=False)

        nn = MLP(1, 1, [2], activation="lrelu")
        optim = torch.optim.Adam(nn.parameters(), lr=0.1)

        list(nn.layers[0].parameters())[0].data = torch.tensor([[-1.0], [-1.0]])
        list(nn.layers[0].parameters())[1].data = torch.tensor([-1.0, -1.0])

        x = torch.linspace(-1, 1, 100).reshape(-1, 1)
        y = x

        loss = float("inf")
        epoch = 0
        while loss > 1e-5:
            first, second = nn.layers

            x1 = nn.activation(first(x))
            x2 = second(x1)

            y11 = x1[:, 0]
            y12 = x1[:, 1]

            loss = F.mse_loss(x2, y)

            if epoch % 50 == 0:
                axs[0][0].plot(x, x.detach().flatten())
                axs[0][1].plot(x, y11.detach().flatten())
                axs[1][1].plot(x, y12.detach().flatten())
                axs[0][2].plot(x, x2.detach().flatten())
                axs[0][2].plot(x, y.detach().flatten())

                plt.draw()
                plt.pause(0.001)

                axs[0][0].clear()
                axs[0][1].clear()
                axs[1][1].clear()
                axs[0][2].clear()
                axs[0][2].clear()

                for _axs in axs:
                    for ax in _axs:
                        ax.set_ylim(-1, 1)
                        ax.set_xlim(-1, 1)

                print(f"Epoch={epoch}. Loss={loss.item()}")
                # for p in nn.parameters():
                #     print(p)

            epoch += 1

            optim.zero_grad()
            loss.backward()
            optim.step()

        axs[0][0].plot(x, x.detach().flatten())
        axs[0][1].plot(x, y11.detach().flatten())
        axs[1][1].plot(x, y12.detach().flatten())
        axs[0][2].plot(x, x2.detach().flatten())
        axs[0][2].plot(x, y.detach().flatten())
        plt.show(block=True)
