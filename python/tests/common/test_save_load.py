import os

import numpy as np

from core.agents import DQNAgent
from environments.pendulum import PendulumEnvironment, PendulumStaticConfiguration, PendulumDynamicConfiguration, \
    configurations2parameters, EnemyDynamicConfiguration, EnemyStaticConfiguration
from rendering import RenderingContext

if __name__ == '__main__':
    with RenderingContext(800, 600) as ctx:
        with PendulumEnvironment(ctx) as env:
            pendulum_static_configuration = PendulumStaticConfiguration(0.15, np.deg2rad(30), 0.5, 0.02)
            pendulum_dynamic_configuration = PendulumDynamicConfiguration(np.deg2rad(30), 0, np.deg2rad(5))

            enemies_static_configurations = [EnemyStaticConfiguration(0.1, 0.25, 0.25)]
            enemies_dynamic_configurations = [EnemyDynamicConfiguration()]

            generated_parameters = configurations2parameters(pendulum_static_configuration,
                                                             enemies_static_configurations,
                                                             pendulum_dynamic_configuration,
                                                             enemies_dynamic_configurations)
            env.setup(generated_parameters)

            m = DQNAgent(env)
            fname = "test.pt"

            m.save(fname)
            m.load(fname)

            # cleanup
            os.remove(fname)
