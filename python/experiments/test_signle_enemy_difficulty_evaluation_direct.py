import numpy as np

from evaluators import DirectEvaluator
from experimentation import Run, experiment


@experiment("Direct evaluator", tags=["Single enemy", "Difficulty evaluation"], wandb=True, clean=True, args={
    "connector_length": 0.5,
    "max_angle": np.linspace(5, 50, 10),
    "enemy_radius": 0.1,
    "bob_radius": 0.15,
    "enemy_x_min": -2.5,
    "enemy_x_max": 2.5,
    "subdivisions": 100,
})
def main(run: Run, connector_length, max_angle, enemy_radius, bob_radius, enemy_x_min, enemy_x_max, subdivisions):
    evaluator = DirectEvaluator(connector_length, np.deg2rad(max_angle), enemy_radius, bob_radius)

    x = np.linspace(enemy_x_min, enemy_x_max, subdivisions)
    difficulties = evaluator.evaluate(x)

    for x, difficulty in zip(x, difficulties):
        run.log(x=x, difficulty=difficulty)


main()
