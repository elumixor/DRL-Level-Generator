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
            enemy_x = -0.10
            generator.enemy_x = enemy_x

            R_best = None
            R_worst = None

            subdivisions = 11

            total_rewards = [[0] * trajectories] * subdivisions
            R_bests = [None] * subdivisions
            R_worsts = [None] * subdivisions

            randomnesses = np.linspace(0, 1, subdivisions)

            run = wandb.init(project="Heuristic", name=f"Boundaries progression", config={
                "Share": True,
                **generator.config
            })

            for r, randomness in enumerate(randomnesses):
                log.good(f"Randomness set to {randomness:.2f}")
                actor.randomness = randomness

                total_rewards[r] = [0] * trajectories

                for t in range(trajectories):
                    state = env.reset()
                    obs = env.get_observation(state)

                    max_len = 75
                    i = 0
                    done = False
                    total_reward = 0

                    while not done and i < max_len:
                        action = actor.get_action(obs)
                        obs, reward, done = env.transition(action)
                        total_reward += reward

                        i += 1

                    if t % (trajectories // 10) == 0:
                        print(f"{t / trajectories * 10:5.2f}%")

                    total_rewards[r][t] = total_reward

                R_bests[r] = max([R_bests[r - 1] if r > 0 else float("-inf"), max(total_rewards[r])])
                R_worsts[r] = min([R_worsts[r - 1] if r > 0 else float("inf"), min(total_rewards[r])])

                wandb.log({"R best": R_bests[r], "R worst": R_worsts[r]})

            run.finish()

            for r in range(subdivisions):
                randomness = randomnesses[r]

                run = wandb.init(project="Heuristic", name=f"Randomness ({randomness:.2f}), shared", config={
                    "Share": True,
                    **generator.config
                })

                for _ in range(0, r):
                    wandb.log({"Difficulty": None})

                for i in range(r, subdivisions):
                    R_best, R_worst = R_bests[i], R_worsts[i]

                    difficulty_run = None
                    if not approx(R_worst, R_best):
                        trajectories_difficulties = [(1 - (total_reward - R_worst) / (R_best - R_worst))
                                                     for total_reward in total_rewards[r]]

                        difficulty_run = sum(trajectories_difficulties) / trajectories

                    wandb.log({"Difficulty": difficulty_run})

                run.finish()
