import time

import glfw

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

        with PendulumEnvironment(ctx, generator, difficulty=0.5) as env:
            actor = HeuristicsPlayer()
            randomness = actor.randomness
            actor.randomness = None

            while True:
                state = env.reset()
                obs = env.get_observation(state)

                if randomness != actor.randomness:
                    log.good(f"Randomness set to {randomness:.2f}")
                    actor.randomness = randomness

                    R_best = None
                    R_worst = None
                    run = None
                    difficulties = 0
                    num_trajectories = 0

                    if run is not None:
                        run.finish()

                    run = wandb.init(project="Heuristic", name=f"Randomness {randomness:.2f}", config={
                        "randomness": randomness
                    })

                max_len = 75
                i = 0
                done = False
                total_reward = 0

                while not done and i < max_len:
                    if ctx.is_key_pressed(glfw.KEY_ESCAPE):
                        exit()

                    if ctx.is_key_held(glfw.KEY_R):
                        randomness = min(1.0, randomness + 0.01)
                        print(f"Randomness={randomness:.2f}")

                    elif ctx.is_key_held(glfw.KEY_D):
                        randomness = max(0.0, randomness - 0.01)
                        print(f"Randomness={randomness:.2f}")

                    env.render()
                    generator.handle_input()

                    action = actor.get_action(obs)
                    obs, reward, done = env.transition(action)
                    total_reward += reward

                    i += 1

                    time.sleep(0.02)

                num_trajectories += 1

                if R_best is None or total_reward > R_best:
                    R_best = total_reward

                if R_worst is None or total_reward < R_worst:
                    R_worst = total_reward

                wandb.log({
                    "Total reward": total_reward,
                    "R_best": R_best,
                    "R_worst": R_worst,
                })

                if not approx(R_worst, R_best):
                    S = (total_reward - R_worst) / (R_best - R_worst)
                    D = 1 - S
                    difficulties += D
                    D_mean = difficulties / num_trajectories
                    print(f"S={S:.2f} D={D:.2f} mean(D)={D_mean}")

                    wandb.log({
                        "Difficulty (trajectory)": D,
                        "Difficulty (run)": D_mean,
                        "Trajectories count": num_trajectories
                    })
