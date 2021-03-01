import numpy as np

import wandb
from common import log
from environments.pendulum import PendulumEnvironment
from environments.pendulum.generators.draggable import DraggableGenerator
from environments.pendulum.heuristics import HeuristicsPlayer
from rendering import RenderingContext
from utilities import approx

if __name__ == '__main__':
    with RenderingContext(800, 600) as ctx:
        generator = DraggableGenerator(ctx)
        trajectories = 1_000

        with PendulumEnvironment(ctx, generator, difficulty=0.5) as env:
            actor = HeuristicsPlayer()

            for x in np.linspace(-0.25, 0.25, 11):
                run = wandb.init(project="Heuristic", name=f"Enemy X = {x:.2f}", config={
                    "x": x
                })

                log(f"x={x:.2f}", bold=True, r=100)
                generator.enemy_x = x

                for randomness in np.linspace(0, 1, 11):
                    log.good(f"Randomness set to {randomness:.2f}")
                    actor.randomness = randomness

                    R_best = None
                    R_worst = None
                    difficulties = 0
                    num_trajectories = 0

                    for t in range(trajectories):
                        state = env.reset()
                        obs = env.get_observation(state)

                        max_len = 75
                        i = 0
                        done = False
                        total_reward = 0

                        while not done and i < max_len:
                            generator.handle_input()

                            action = actor.get_action(obs)
                            obs, reward, done = env.transition(action)
                            total_reward += reward

                            i += 1

                        num_trajectories += 1

                        if R_best is None or total_reward > R_best:
                            R_best = total_reward

                        if R_worst is None or total_reward < R_worst:
                            R_worst = total_reward

                        if not approx(R_worst, R_best):
                            S = (total_reward - R_worst) / (R_best - R_worst)
                            D = 1 - S
                            difficulties += D

                        if t % (trajectories // 10) == 0:
                            print(f"{t / trajectories * 100:.2}%")

                    wandb.log({
                        "R_best": R_best,
                        "R_worst": R_worst,
                        "Difficulty": difficulties / num_trajectories,
                        "Enemy x": x,
                        "Randomness": randomness
                    })

                run.finish()
