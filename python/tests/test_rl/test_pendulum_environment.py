import numpy as np

from core import train, Trajectory, evaluate
from core.agents.dqn import DQNAgent
from environments.pendulum import configurations2parameters, PendulumStaticConfiguration, EnemyStaticConfiguration, \
    PendulumDynamicConfiguration, EnemyDynamicConfiguration, PendulumEnvironment
from rendering import RenderingContext

if __name__ == '__main__':
    with RenderingContext(800, 600) as rc:
        with PendulumEnvironment(rc) as env:
            pendulum_static_configuration = PendulumStaticConfiguration(0.15, np.deg2rad(30), 0.5, 0.02)
            pendulum_dynamic_configuration = PendulumDynamicConfiguration(np.deg2rad(30), 0, np.deg2rad(5))

            enemies_static_configurations = [EnemyStaticConfiguration(0.1, 0.25, 0.25)]
            enemies_dynamic_configurations = [EnemyDynamicConfiguration()]

            generated_parameters = configurations2parameters(pendulum_static_configuration,
                                                             enemies_static_configurations,
                                                             pendulum_dynamic_configuration,
                                                             enemies_dynamic_configurations)
            env.setup(generated_parameters)

            agent = DQNAgent(env, epsilon_iterations=100, buffer_capacity=100000)
            train(env, agent, epochs=100, num_trajectories=5, render_frequency=25, cutoff_at=75)
            evaluate(env, agent, cutoff_at=75)
