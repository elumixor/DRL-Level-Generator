import numpy as np

from experiments import run_current


def main(context, max_angle, subdivisions, enemy_x_min, enemy_x_max, enemy_radius, bob_radius,
         connector_length):
    max_angle = np.deg2rad(max_angle)
    x_p_max = connector_length * np.sin(max_angle)

    def calculate_difficulty(x_l):
        s_left = min(max(x_l - enemy_radius - bob_radius + x_p_max, 0), 2 * x_p_max)
        s_right = min(max(x_p_max - x_l - enemy_radius - bob_radius, 0), 2 * x_p_max)

        return 1 - (s_left + s_right) / (2 * x_p_max)

    difficulties = [calculate_difficulty(x_l) for x_l in np.linspace(enemy_x_min, enemy_x_max, subdivisions)]

    for d, x_l in zip(difficulties, np.linspace(enemy_x_min, enemy_x_max, subdivisions)):
        context.log({"x": x_l, "difficulty": d})


if __name__ == '__main__':
    run_current(console=True, args={
        "max_angle": 0.1
    })
