import numpy as np

from evaluators import DirectEvaluator
from experiments import run_current


def main(context, max_angle, subdivisions, enemy_x_min, enemy_x_max, enemy_radius, bob_radius, connector_length):
    evaluator = DirectEvaluator(connector_length, np.deg2rad(max_angle), enemy_radius, bob_radius)

    x = np.linspace(enemy_x_min, enemy_x_max, subdivisions)
    difficulties = evaluator.evaluate(x)

    for x, difficulty in zip(x, difficulties):
        context.log({"x": x, "difficulty": difficulty})


if __name__ == '__main__':
    run_current(console=True,
                # args={"max_angle": 30}
                )
