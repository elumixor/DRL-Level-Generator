import glfw
import numpy as np
import torch

from environments import PendulumEnvironment
from environments.pendulum import configurations2parameters, PendulumStaticConfiguration, EnemyStaticConfiguration, \
    PendulumDynamicConfiguration, EnemyDynamicConfiguration
from rendering import RenderingContext

if __name__ == '__main__':
    with RenderingContext(800, 600) as rc:
        with PendulumEnvironment(rc) as env:
            pendulum_static_configuration = PendulumStaticConfiguration(0.35, np.deg2rad(30), 0.5, 0.02)
            pendulum_dynamic_configuration = PendulumDynamicConfiguration(np.deg2rad(30), 0, np.deg2rad(5))

            enemies_static_configurations = [EnemyStaticConfiguration(0.25, 0.25, 0.25)]
            enemies_dynamic_configurations = [EnemyDynamicConfiguration()]

            generated_parameters = configurations2parameters(pendulum_static_configuration,
                                                             enemies_static_configurations,
                                                             pendulum_dynamic_configuration,
                                                             enemies_dynamic_configurations)
            env.setup(generated_parameters)
            env.reset()
            env.render()
            done = False
            while not done:
                rc.render_frame()
                if rc.is_key_down(glfw.KEY_ESCAPE):
                    break

                action = None

                if rc.is_key_down(glfw.KEY_N):
                    action = 0.0
                elif rc.is_key_down(glfw.KEY_SPACE):
                    action = 1.0

                if action is None:
                    continue

                env.transition(torch.tensor([action]))
                env.render()
