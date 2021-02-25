import numpy as np

from core.agents import DQNAgent
from core.utils import EpsilonDecay
from environments.pendulum import PendulumEnvironment, PendulumGenerator, PendulumState
from rendering import RenderingContext

if __name__ == '__main__':
    with RenderingContext(800, 600) as rc:
        class G(PendulumGenerator):
            def generate(self, difficulty: float, seed: float) -> PendulumState:
                bob_radius = 0.15
                max_angle = np.deg2rad(30)
                connector_length = 0.5
                vertical_speed = 0.02

                enemy_radius = 0.1
                enemy_x = -0.25 * seed + 0.25 * (1 - seed)
                enemy_x = 0.25
                enemy_y = 0.25

                angle = np.deg2rad(30)
                position = 0
                angular_speed = np.deg2rad(5)

                return PendulumState(bob_radius, max_angle, connector_length, vertical_speed,
                                     enemy_x, enemy_y, enemy_radius,
                                     angle, position, angular_speed)


        with PendulumEnvironment(rc, G(), difficulty=0.5) as env:
            agent = DQNAgent(env, maximum_length=75, epsilon_decay=EpsilonDecay(iterations=50000))

            agent.train(epochs=1000, render_frequency=25, validation_frequency=10, num_validation_trajectories=25)

            # evaluate(env, agent, maximum_length=75)
