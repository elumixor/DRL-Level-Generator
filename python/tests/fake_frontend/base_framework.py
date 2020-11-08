# For each epoch, we will play several rollouts, collect samples and train
import math
import time
from typing import Optional

from numpy import mean

from utilities import Plotter


def train(env,
          agent_class,
          epochs: int = 100,
          num_rollouts: int = 1,
          max_timesteps: int = -1,
          print_frequency: int = 1,
          tests: int = None,
          render_frequency: Optional[int] = None,
          plot_frequency: Optional[int] = None,
          seed: Optional[int] = None):
    """
    Generalized training function.

    --------------------------------------------------------------------------------------------------------------------

    For each epoch, creates several rollouts (trajectories) of the given environment.

    Requires get_action(state) function to determine an action for the given state and let an agent act in the
    environment, and update_agent(trajectories), that is called at the end of an epoch - when all rollouts have finished
    to train an agent.

    --------------------------------------------------------------------------------------------------------------------

    :param env: OpenAI gym environment

    :param agent_class: Agent instance to be acting in the environment

    :param epochs: Number of epochs to train

    :param num_rollouts: Number of trajectories per epoch

    :param print_frequency: How often will the results be printed.
                            For example, if set to 5, will print results every 5 epochs

    :param render_frequency: How often will the environment be rendered. This number is shared across trajectories
                             and epochs. For example, if set to 5, and number of trajectories is 3, will render at
                             (epoch 0, traj. 0), (epoch 1, traj. 1), (epoch 2, traj. 0)  ...

    :param max_timesteps: Maximum timesteps per trajectory. If the rollout is too long (for example, when agent performs
                          well, this will cut of the rollout, so we don't have infinitely long rollouts

    :param plot_frequency: How often should the results be plotted

    :param tests: How many test should run on the trained model, or None

    :param seed: Custom seed, or None
    """
    if max_timesteps < 0:
        max_timesteps = math.inf

    if seed is not None:
        env.seed(seed)

    plotter = Plotter()
    plotter['reward'].name = "Mean total epoch reward"

    total_time = 0.
    epochs_time = 0.

    start_time = time.time()
    agent = agent_class(env)

    global_rollout = 0
    for epoch in range(epochs):
        rollouts = []
        rollout_rewards = []

        for rollout in range(num_rollouts):
            state = env.reset()
            done = False

            agent.on_trajectory_started(state)

            total_reward = 0

            t = 0
            while not done and t < max_timesteps:
                if render_frequency and global_rollout % render_frequency == 0:
                    env.render()

                action = agent.get_action(state)
                state, reward, done, _ = env.step(action)
                agent.save_step(action, reward, state)

                t += 1
                total_reward += reward

            agent.on_trajectory_finished()

            rollout_rewards.append(total_reward)
            global_rollout += 1

        agent.update()

        plotter['reward'] += mean(rollout_rewards)

        end_time = time.time()
        epochs_time += end_time - start_time
        start_time = end_time

        if epoch % print_frequency == 0:
            total_time += epochs_time

            print(f'Epoch\t{epoch} \t| '
                  f'{total_time:.02f}s \t| '
                  f'Mean total reward\t{mean(plotter["reward"].y[-print_frequency:]):.4f}')

            epochs_time = 0.

        if plot_frequency is not None and epoch % plot_frequency == 0:
            plotter.show("reward", running_average=True)

    # Display the performance of the trained model for several times
    if tests is not None:
        agent.set_to_evaluation_mode()
        for t in range(tests):
            state = env.reset()

            total_reward = 0
            step = 0
            while step < max_timesteps:
                env.render()

                action = agent.get_action(state)
                state, reward, done, _ = env.step(action)
                total_reward += reward
                step += 1
                if done:
                    break

            print(f'Test {t}: total reward: {total_reward}')
