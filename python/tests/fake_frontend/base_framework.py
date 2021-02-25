# For each epoch, we will play several rollouts, collect samples and train
import math
from typing import Optional


def train(env,
          agent_class,
          epochs: int = 100,
          num_rollouts: int = 1,
          max_timesteps: int = -1,
          render_frequency: Optional[int] = None,
          seed: Optional[int] = None):
    """
    Generalized training function.

    --------------------------------------------------------------------------------------------------------------------

    For each epoch, creates several rollouts (trajectories) of the given environment.

    Requires get_action(observation) function to determine an action for the given observation and let an agent act in the
    environment, and update_agent(trajectories), that is called at the end of an epoch - when all rollouts have finished
    to train an agent.

    --------------------------------------------------------------------------------------------------------------------

    :param env: OpenAI gym environment

    :param agent_class: Agent instance to be acting in the environment

    :param epochs: Number of epochs to train

    :param num_rollouts: Number of trajectories per epoch

    :param render_frequency: How often will the environment be rendered. This number is shared across trajectories
                             and epochs. For example, if set to 5, and number of trajectories is 3, will render at
                             (epoch 0, traj. 0), (epoch 1, traj. 1), (epoch 2, traj. 0)  ...

    :param max_timesteps: Maximum timesteps per trajectory. If the rollout is too long (for example, when agent performs
                          well, this will cut of the rollout, so we don't have infinitely long rollouts

    :param seed: Custom seed, or None
    """
    if max_timesteps < 0:
        max_timesteps = math.inf

    if seed is not None:
        env.seed(seed)

    agent = agent_class(env)

    global_rollout = 0
    for epoch in range(epochs):
        rollout_rewards = []

        for rollout in range(num_rollouts):
            state = env.reset()
            done = False

            agent.on_trajectory_started(state)

            total_reward = 0

            t = 0
            do_render = render_frequency and global_rollout != 0 and global_rollout % render_frequency == 0
            if do_render:
                agent.eval()
            while not done and t < max_timesteps:
                if do_render:
                    env.render()

                action = agent.get_action(state)
                state, reward, done, *_ = env.step(action)
                agent.save_step(action, reward, done, state)

                t += 1
                total_reward += reward

            if do_render:
                print(total_reward)
                agent.print_progress()
                agent.plot_progress()
                agent.train()

            agent.on_trajectory_finished()

            rollout_rewards.append(total_reward)
            global_rollout += 1

        agent.train()
