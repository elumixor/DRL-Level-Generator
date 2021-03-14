import matplotlib.pyplot as plt
import numpy as np
import torch
import wandb

from environments.pendulum.generators import SimpleNNGenerator

plt.ioff()

if __name__ == '__main__':
    for a in np.linspace(5, 50, 5):
        generator = SimpleNNGenerator(max_angle=np.deg2rad(a))

        x_max, x_min = generator.max_x, generator.min_x
        r_enemy = generator.enemy_radius
        r_bob = generator.bob_radius
        c = generator.connector_length

        x_p_max = generator.connector_length * np.sin(generator.max_angle)


        def calculate_difficulty(x_l: torch.Tensor):
            s_left = torch.clamp(x_l - r_enemy - r_bob + x_p_max, 0, 2 * x_p_max)
            s_right = torch.clamp(x_p_max - x_l - r_enemy - r_bob, 0, 2 * x_p_max)

            return 1 - (s_left + s_right) / (2 * x_p_max)


        def calculate_diversity(d_in: torch.Tensor, enemy_x: torch.Tensor):
            # s = torch.tensor([0.0])
            # for i in range(d_in.shape[0]):
            #     for j in range(i + 1, d_in.shape[0]):
            #         s = s + torch.abs(enemy_x[i] - enemy_x[j]) * torch.abs(d_in[i] - d_in[j])

            # Same as above, but not O(n^2)
            n = d_in.shape[0]
            return ((enemy_x - enemy_x.T).abs() * (d_in - d_in.T).abs()).triu().sum() * 2 / (n * (n - 1))


        epochs = 1000
        batch_size = 250

        run = wandb.init(project="Heuristic", name="Training Heuristic 1", tags=["Diversity"], config={
            "epochs": epochs,
            "batch size": batch_size,
            **generator.config
        })
        run.config.update({"Max angle": np.rad2deg(generator.max_angle)}, allow_val_change=True)

        wandb.watch(generator.nn)

        for epoch in range(epochs):
            d_in = torch.rand(batch_size, 1)
            enemy_x = generator.generate(d_in)
            d_out = calculate_difficulty(enemy_x)

            diversity = calculate_diversity(d_in, enemy_x)

            loss_difficulty, loss_diversity = generator.update(d_in, d_out, diversity)

            wandb.log({
                "loss difficulty": loss_difficulty,
                "diversity": loss_diversity,
                "loss difficulty - diversity": loss_difficulty - loss_diversity
            })

        run.finish()
