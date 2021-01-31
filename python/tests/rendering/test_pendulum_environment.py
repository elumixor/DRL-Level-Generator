import numpy as np

from environments import PendulumEnvironment
from environments.pendulum import configurations2parameters, PendulumStaticConfiguration, EnemyStaticConfiguration, \
    PendulumDynamicConfiguration, EnemyDynamicConfiguration
from rendering import RenderingContext

if __name__ == '__main__':
    with RenderingContext(800, 600) as rc:
        with PendulumEnvironment(rc) as pendulum:
            pendulum_static_configuration = PendulumStaticConfiguration(0.35, np.deg2rad(30), 0.5, 0.5)
            pendulum_dynamic_configuration = PendulumDynamicConfiguration(np.deg2rad(30), 0, np.deg2rad(10))

            enemies_static_configurations = [EnemyStaticConfiguration(0.25, 0.25, 0.25)]
            enemies_dynamic_configurations = [EnemyDynamicConfiguration()]

            generated_parameters = configurations2parameters(pendulum_static_configuration,
                                                             enemies_static_configurations,
                                                             pendulum_dynamic_configuration,
                                                             enemies_dynamic_configurations)
            pendulum.setup(generated_parameters)
            pendulum.reset()
            pendulum.render()

            # Keeps rendering the last frame, waits for exit
            rc.render()
