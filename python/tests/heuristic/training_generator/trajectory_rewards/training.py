import random

import torch
from scipy.stats import skewnorm

from environments.pendulum import PendulumEnvironment
from environments.pendulum.generators import NNGenerator
from environments.pendulum.heuristics import HeuristicsPlayer
from rendering import RenderingContext

if __name__ == '__main__':
    with RenderingContext(800, 600) as ctx:
        generator = NNGenerator()
        with PendulumEnvironment(ctx, generator) as env:
            epochs = 2
            batch_size = 2
            trajectories = 2
            max_len = 75

            randomnesses = torch.tensor([0, 0.125, 0.25, 0.375, 0.5])

            policies = [HeuristicsPlayer()] * len(randomnesses)
            for policy, r in zip(policies, randomnesses):
                policy.randomness = r

            zipped = [*zip(randomnesses, policies, range(len(policies)))]

            alpha = 2
            loc = 0.75
            scale = 0.5

            cdf_0 = skewnorm.cdf(0, alpha, loc=loc, scale=scale)
            cdf_1 = skewnorm.cdf(1, alpha, loc=loc, scale=scale)
            diff = cdf_1 - cdf_0


            def get_weight(epsilon):
                return skewnorm.pdf(epsilon, alpha, loc=loc, scale=scale) / diff


            weights = [float(get_weight(epsilon)) for epsilon in randomnesses]
            s = sum(weights)
            weights = [weight / s for weight in weights]

            # for a in np.linspace(5, 50, 5):
            total_trajectories = epochs * batch_size * len(policies) * trajectories
            t = 0

            for a in [30]:

                # Main loop
                # run = wandb.init(project="Heuristic", name="Training Heuristic 1", tags=["Diversity"], config={
                #     "epochs": epochs,
                #     "batch size": batch_size,
                #     **generator.config
                # })
                # run.config.update({"Max angle": np.rad2deg(generator.max_angle)}, allow_val_change=True)
                #
                # wandb.watch(generator.nn)

                for epoch in range(epochs):
                    loss = 0

                    for batch in range(batch_size):
                        d_in = random.random()
                        level = generator.generate(d_in)

                        total_rewards = [0] * len(policies)

                        R_max = float("-inf")
                        R_min = float("inf")

                        for epsilon, policy, i in zipped:
                            total_reward = 0

                            for trajectory in range(trajectories):
                                if t % 1000 == 0:
                                    print(f" {t / total_trajectories * 100:5.2f}% [{t}/{total_trajectories}]")
                                t += 1

                                state = env.reset(d_in)
                                obs = env.get_observation(state)

                                done = False
                                trajectory_reward = 0

                                for _ in range(max_len):
                                    action = policy.get_action(obs)
                                    obs, reward, done = env.transition(action)
                                    trajectory_reward += reward

                                    if done:
                                        break

                                total_reward += trajectory_reward

                                # todo back-prop?
                                if trajectory_reward > R_max:
                                    R_max = trajectory_reward

                                if trajectory_reward < R_min:
                                    R_min = trajectory_reward

                            total_rewards[i] = total_reward

                        diff = R_max - R_min

                        difficulties = [weights[i] * (R_max - total_rewards[i] / trajectories) / diff for _, _, i in
                                        zipped]
                        difficulty = sum(difficulties)
                        print(d_in, difficulty)

                        loss += (difficulty - d_in) ** 2

                    loss /= batch_size

                    print(f"UPDATING!!!! {loss}")
                    generator.update(loss)
                    # total_rewards[r][t] = total_reward
                    # d_out = calculate_difficulty(enemy_x)
                    #
                    # diversity = calculate_diversity(d_in, enemy_x)
                    #
                    # loss_difficulty, loss_diversity = generator.update(d_in, d_out, diversity)

                #     wandb.log({
                #         "loss difficulty": loss_difficulty,
                #         "diversity": loss_diversity,
                #         "loss difficulty - diversity": loss_difficulty - loss_diversity
                #     })
                #
                # run.finish()
