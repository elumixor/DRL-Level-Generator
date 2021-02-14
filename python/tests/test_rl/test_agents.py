import cProfile
import pstats

import numpy as np

from core import train
from core.agents import A2CAgent
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

            AgentClass = A2CAgent

            agent = AgentClass(env)

            profiler = cProfile.Profile()
            profiler.enable()
            train(env, agent, epochs=50, num_trajectories=10, render_frequency=25, cutoff_at=75)
            profiler.disable()
            pstats.Stats(profiler).sort_stats('tottime').print_stats()

            # evaluate(env, agent, cutoff_at=75)
