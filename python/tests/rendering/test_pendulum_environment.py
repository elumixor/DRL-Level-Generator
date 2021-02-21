import glfw
import numpy as np
import torch

from environments.pendulum import PendulumEnvironment, PendulumState, PendulumGenerator
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
                enemy_x = 0.25
                enemy_y = 0.25

                angle = np.deg2rad(30)
                position = 0
                angular_speed = np.deg2rad(5)

                return PendulumState(bob_radius, max_angle, connector_length, vertical_speed,
                                     enemy_x, enemy_y, enemy_radius,
                                     angle, position, angular_speed)


        with PendulumEnvironment(rc, G()) as env:
            env.reset(0.5)
            env.render()
            done = False
            while not done:
                rc.render_frame()
                if rc.is_key_pressed(glfw.KEY_ESCAPE):
                    break

                action = None

                if rc.is_key_pressed(glfw.KEY_N):
                    action = 0.0
                elif rc.is_key_pressed(glfw.KEY_SPACE):
                    action = 1.0

                if action is None:
                    continue

                _, reward, done = env.transition(torch.tensor([action]))
                print(f"Action={action} Reward={reward}")
                env.render()
