import matplotlib.pyplot as plt
import numpy as np
import wandb

from environments.pendulum.generators.draggable import DraggableGenerator
from rendering import RenderingContext

plt.ioff()

if __name__ == '__main__':
    with RenderingContext(800, 600) as ctx:
        for a in np.linspace(5, 50, 5):
            generator = DraggableGenerator(ctx, max_angle=np.deg2rad(a))

            x_max, x_min = generator.max_x, generator.min_x
            r_enemy = generator.enemy_radius
            r_bob = generator.bob_radius
            c = generator.connector_length

            x_p_max = generator.connector_length * np.sin(generator.max_angle)


            def calculate_difficulty(x_l):
                s_left = min(max(x_l - r_enemy - r_bob + x_p_max, 0), 2 * x_p_max)
                s_right = min(max(x_p_max - x_l - r_enemy - r_bob, 0), 2 * x_p_max)

                return 1 - (s_left + s_right) / (2 * x_p_max)


            difficulties = [calculate_difficulty(x_l) for x_l in np.linspace(x_min, x_max, 101)]

            # plt.plot(difficulties)
            # plt.show()

            run = wandb.init(project="Heuristic", name="Heuristic 1", config=generator.config)
            run.config.update({"Max angle": np.rad2deg(generator.max_angle)}, allow_val_change=True)

            for d, x_l in zip(difficulties, np.linspace(x_min, x_max, 101)):
                run.log({"x": x_l, "difficulty": d})

            run.finish()
