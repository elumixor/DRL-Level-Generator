import sys

import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.distributions import Normal
from torch.nn import Module, Linear, Softplus, LeakyReLU
# let us have a difficulty function as follows:
from torch.optim import Adam

from common.printing import log

x_min = -2
x_max = 2


def D(x):
    return np.clip(-(np.abs(x) - 1.1), 0.0, 1.0)


def visualize_D():
    fig, axs = plt.subplots(1, 1)
    x = np.linspace(x_min, x_max, 100)
    y = D(x)

    axs.plot(x, y)

    plt.show()


def train(nn, optim, epochs=2000, d_in_size=100, samples=25):
    print_epoch = epochs // 10

    for epoch in range(epochs):
        d_in = torch.linspace(0, 1, d_in_size).unsqueeze(-1)

        mean, std = nn(d_in)
        dist = Normal(mean, std)

        sample = dist.sample([samples])
        log_prob = dist.log_prob(sample)

        d_out = D(sample)

        loss = ((d_out - d_in).abs() * log_prob).mean()

        optim.zero_grad()
        loss.backward()

        with torch.no_grad():
            total_grad = 0

            for p in nn.parameters():
                total_grad += p.grad.abs().mean()

        optim.step()

        with torch.no_grad():
            test = (D(mean) - d_in).abs().mean()

        if epoch % print_epoch == 0:
            print(f"{epoch:6} {epoch / epochs * 100:>5.0f}% {test:10.5f} {total_grad:10.5f}")

        if test < 0.01:
            log.good(f"Required accuracy reached at:")
            print(f"{epoch:6} {epoch / epochs * 100:>5.0f}% {test:10.5f}")
            return True

    return False


def draw():
    ax.clear()

    mean, std = nn(torch.tensor([d_in]))

    dist = Normal(mean.flatten(), std.flatten())

    x = torch.from_numpy(np.linspace(-2, 2, 1000))

    p_x = dist.log_prob(x).exp()

    ax.plot(x, p_x)
    ax.plot(x, D(x))

    ax.plot([mean, mean], [0, dist.log_prob(mean.flatten()).exp()])
    ax.plot([x_min, x_max], [d_in, d_in])

    ax.set_title(f"D = {d_in:.2f} mean = {mean.item():.2f}")


if __name__ == '__main__':
    class NN(Module):
        def __init__(self, min_std=0.01):
            super().__init__()

            self.l1 = Linear(1, 4)
            self.l2 = Linear(4, 4)

            self.mean = Linear(4, 1)
            self.std = Linear(4, 1)
            self.softplus = Softplus()

            self.lrelu = LeakyReLU()

            self.min_std = min_std

        def forward(self, x):
            x = self.l1(x)
            x = self.lrelu(x)
            x = self.l2(x)
            x = self.lrelu(x)

            mean = self.mean(x)
            std = self.std(x)
            std = self.softplus(std) + self.min_std

            return mean, std


    # Get the poorly initialized model
    succeeded = True
    while succeeded:
        nn = NN()
        optim = Adam(nn.parameters(), lr=0.01)
        succeeded = train(nn, optim)

    # for p in nn.parameters():
    #     print(p)
    #
    # x = torch.tensor([0.5])
    # print(x)
    # x = nn.l1(x).relu()
    # print(x)
    # x = nn.l2(x).relu()
    # print(x)
    # print()
    # mean = nn.mean(x)
    # print(mean)
    # print()
    # std = nn.std(x)
    # print(std)
    # std = nn.softplus(std) + 0.01
    # print(std)

    with torch.no_grad():
        d_in = 0.5

        fig, ax = plt.subplots()


        def on_press(event):
            sys.stdout.flush()

            triggered = event.key == "left" or event.key == "right"

            if not triggered:
                return

            global d_in

            d_in = max(0.0, d_in - 0.1) if event.key == "left" else min(1.0, d_in + 0.1)

            draw()
            fig.canvas.draw()


        fig.canvas.mpl_connect('key_press_event', on_press)

        draw()

        plt.show()
