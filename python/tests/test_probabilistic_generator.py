import matplotlib.pyplot as plt
import numpy as np
import torch
from scipy.stats import truncnorm
from torch.nn import Module, Linear, Softplus
from torch.optim import Adam

import wandb
from common import Clamp
from rendering import RenderingContext, Circle, Color


class Generator(Module):
    def __init__(self, min, max):
        super().__init__()

        self.base = Linear(1, 4)
        self.head_mean = Linear(4, 1)
        self.head_std = Linear(4, 1)
        self.softplus = Softplus()
        self.remap = Clamp(min, max)

    def forward(self, difficulty):
        hidden = self.base(difficulty)
        mean = self.head_mean(hidden)
        mean = mean.sigmoid()
        mean = self.remap(mean)

        std = self.head_std(hidden)
        std = self.softplus(std)

        return mean, std


if __name__ == '__main__':
    with RenderingContext(800, 600) as ctx:
        x_player = 0.0
        r_player = 0.05

        player = Circle(Color.green, radius=r_player, parent=ctx.main_scene)
        player.x = x_player

        x_enemy = 0.1
        r_enemy = 0.05

        x_min = -1
        x_max = 1

        enemy = Circle(Color.red, radius=r_enemy, parent=ctx.main_scene)
        enemy.x = x_enemy

        generator = Generator(x_min, x_max)
        lr = 0.01
        optim = Adam(generator.parameters(), lr=lr)

        diff = 0.5

        num_samples_input_difficulty = 25
        num_samples_levels = 50


        def generate(plot=False):
            with torch.no_grad():
                mean, std = generator(torch.tensor([diff]))

            a, b = (x_min - mean) / std, (x_max - mean) / std
            sample = truncnorm.rvs(a, b)
            result = torch.tensor(sample, dtype=torch.float32)
            result = result * std + mean

            enemy.x = result

            if plot:
                plot_dist(mean, std)


        def difficulty():
            return abs(enemy.x - player.x)


        def plot_dist(mean, std):
            mean = mean.item()
            std = std.item()

            print(f"mean={mean:.4f}, std={std:.4f}")

            x = np.linspace(-1.5, 1.5, 101)
            a, b = (x_min - mean) / std, (x_max - mean) / std
            y = truncnorm.pdf(x, a, b, mean, std)
            plt.plot(x, y)
            plt.show()


        def train():
            # d_in = torch.rand([num_samples_input_difficulty, 1])
            d_in = torch.linspace(0, 1, num_samples_input_difficulty).reshape([-1, 1])

            with torch.no_grad():
                mean, std = generator(d_in)

            a, b = (x_min - mean) / std, (x_max - mean) / std

            sample = truncnorm.rvs(a, b, size=[a.shape[0], num_samples_levels])
            result = torch.tensor(sample, dtype=torch.float32)
            result = result * std + mean

            d_out = torch.abs(result - player.x)

            difficulty_difference = torch.abs(d_in - d_out)

            log_probabilities = torch.zeros_like(result)
            means, stds = generator(d_in)

            for i, (mean, std, g) in enumerate(zip(means, stds, result)):
                dist = torch.distributions.Normal(loc=mean, scale=std)

                # Truncate
                cdf_min = dist.cdf(x_min)
                cdf_max = dist.cdf(x_max)

                lp = dist.log_prob(g) - torch.log(cdf_max - cdf_min)
                log_probabilities[i] = lp

            loss = (difficulty_difference * log_probabilities).mean()
            wandb.log({
                "difficulty differences": difficulty_difference.mean(),
                "loss": loss
            })

            optim.zero_grad()
            loss.backward()
            optim.step()


        run = wandb.init(project="Heuristic", name="REINFORCE", config={
            "limit": "clamp",
            "num_samples_input_difficulty": num_samples_input_difficulty,
            "num_samples_levels": num_samples_levels,
            "lr": lr,
            "systematic": True
        })

        for _ in range(10000):
            train()

        run.finish()

        # while not ctx.is_key_held(glfw.KEY_ESCAPE):
        #     ctx.render_frame()
        #
        #     if ctx.is_key_pressed(glfw.KEY_G):
        #         generate(ctx.is_key_held(glfw.KEY_LEFT_SHIFT))
        #         print(difficulty())
        #
        #     if ctx.is_key_pressed(glfw.KEY_T):
        #         for _ in range(100 if ctx.is_key_held(glfw.KEY_LEFT_SHIFT) else 10):
        #             train()
        #
        #     if ctx.is_key_pressed(glfw.KEY_LEFT):
        #         diff -= 0.1
        #         generate()
        #
        #     elif ctx.is_key_pressed(glfw.KEY_RIGHT):
        #         diff += 0.1
        #         generate()
