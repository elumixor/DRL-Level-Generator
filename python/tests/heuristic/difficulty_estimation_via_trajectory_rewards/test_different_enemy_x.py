import numpy as np
import wandb

from common import log
from environments.pendulum import PendulumEnvironment
from environments.pendulum.generators.draggable import DraggableGenerator
from environments.pendulum.heuristics import HeuristicsPlayer
from rendering import RenderingContext

if __name__ == '__main__':
    with RenderingContext(800, 600) as ctx:
        generator = DraggableGenerator(ctx)
        num_trajectories = 1_000

        with PendulumEnvironment(ctx, generator, difficulty=0.5) as env:
            actor = HeuristicsPlayer()

            # We'll test different x positions of the enemy
            for x in np.linspace(-0.25, 0.25, 11):
                log(f"x={x:.2f}", bold=True, r=100)
                generator.enemy_x = x

                R_best = float("-inf")
                R_worst = float("inf")

                policies_total_rewards = []

                # We'll evaluate policies with different randomnesses
                for randomness in np.linspace(0, 1, 11):
                    log.good(f"Randomness set to {randomness:.2f}")
                    actor.randomness = randomness

                    policy_reward = 0

                    for t in range(num_trajectories):
                        state = env.reset()
                        obs = env.get_observation(state)

                        max_len = 75
                        i = 0
                        done = False
                        trajectory_reward = 0

                        while not done and i < max_len:
                            action = actor.get_action(obs)
                            obs, reward, done = env.transition(action)
                            trajectory_reward += reward

                            i += 1

                        # Accumulate total reward across all trajectories of the policy
                        policy_reward += trajectory_reward

                        # Update R_best R_worst if needed
                        if trajectory_reward > R_best:
                            R_best = trajectory_reward

                        if trajectory_reward < R_worst:
                            R_worst = trajectory_reward

                        if t % (num_trajectories // 10) == 0:
                            print(f"{t / num_trajectories * 100:6.2f}%")

                    policies_total_rewards.append(policy_reward)

                run = wandb.init(project="Heuristic", name=f"Enemy X {x:.2f}", config={
                    "R best": R_best,
                    "R worst": R_worst,
                    **generator.config
                })

                # Calculate the estimated total rewards with the R_best R_worst of the all policies
                for policy_reward, randomness in zip(policies_total_rewards, np.linspace(0, 1, 11)):
                    # Calculate the experienced difficulty of that policy, given the total reward
                    difficulty_policy = (R_best - policy_reward / num_trajectories) / (R_best - R_worst)

                    wandb.log({
                        "Total policy reward": policy_reward,
                        "Difficulty": difficulty_policy,
                        "Randomness": randomness
                    })

                run.finish()
