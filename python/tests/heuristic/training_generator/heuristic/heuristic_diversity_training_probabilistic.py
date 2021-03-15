import matplotlib.pyplot as plt
import numpy as np
import torch
import wandb

from environments.pendulum.generators import SimpleProbabilisticNNGenerator

plt.ioff()

if __name__ == '__main__':
    for a in np.linspace(5, 50, 5):
        generator = SimpleProbabilisticNNGenerator(max_angle=np.deg2rad(a))

        x_max, x_min = generator.max_x, generator.min_x
        r_enemy = generator.enemy_radius
        r_bob = generator.bob_radius
        c = generator.connector_length

        x_p_max = generator.connector_length * np.sin(generator.max_angle)


        @torch.no_grad()
        def calculate_difficulty(x_l: torch.Tensor):
            s_left = torch.clamp(x_l - r_enemy - r_bob + x_p_max, 0, 2 * x_p_max)
            s_right = torch.clamp(x_p_max - x_l - r_enemy - r_bob, 0, 2 * x_p_max)

            return 1 - (s_left + s_right) / (2 * x_p_max)


        epochs = 1000
        batch_size = 250

        run = wandb.init(project="Heuristic", name="Training Heuristic 1", config={
            "epochs": epochs,
            "batch size": batch_size,
            "backpropagation": "REINFORCE",
            "diversity": True,
            **generator.config
        })

        # To convert radians to degrees
        run.config.update({"Max angle": np.rad2deg(generator.max_angle)}, allow_val_change=True)

        # wandb.watch(generator.nn)

        for epoch in range(epochs):
            d_in = torch.rand([batch_size, 1])
            x, x_clamped = generator.generate(d_in)

            d_out = calculate_difficulty(x_clamped)

            generator.update(d_in, d_out, x)

            if epoch % 10 == 0:
                print(f"{epoch}/{epochs}")

        run.finish()
