import numpy as np
from numba import float32
from numba.experimental import jitclass

import state as State


@jitclass([
    ("const_state", float32[:]),
    ("state", float32[:])
])
class Environment:
    def __init__(self, enemy_x, bob_radius, max_angle, connector_length, vertical_speed,
                 enemy_y, enemy_radius, current_angle, position, angular_speed):
        self.const_state = np.array([bob_radius, max_angle, connector_length, vertical_speed, enemy_x, enemy_y,
                                     enemy_radius, current_angle, position, angular_speed], dtype=np.float32)
        self.state = self.state

    def set_level(self, x):
        self.const_state[State.enemy_x] = x
        self.state = self.const_state

    def reset(self):
        self.state = self.const_state
        return self.state

    def step(self, action):
        switch = action == 1

        # Interpret data
        bob_radius, max_angle, connector_length, vertical_speed, \
        enemy_x, enemy_y, enemy_radius, \
        angle, position, angular_speed = self.state

        if switch:
            angular_speed = angular_speed * -1

        # Add angular movement
        angle = angle + angular_speed

        if np.abs(angle) > max_angle:
            angle = np.sign(angle) * (max_angle - (np.abs(angle) - max_angle))
            angular_speed = angular_speed * -1

        # Add vertical movement
        position = position + vertical_speed

        # Combine into the new observation
        new_state = State.create(bob_radius, max_angle, connector_length, vertical_speed, enemy_x, enemy_y,
                                 enemy_radius, angle, position, angular_speed)

        # Update internal state
        self.state = new_state

        # Check collision
        bob_center_x = np.sin(angle) * connector_length
        bob_center_y = position - np.cos(angle) * connector_length

        reward = 1.0 if not switch else 0.9

        distance = np.sqrt((bob_center_x - enemy_x) ** 2 + (bob_center_y - enemy_y) ** 2)

        # Collision
        if distance <= (bob_radius + enemy_radius):
            done = True
            reward = 0.0 if not switch else -0.1
            return new_state, reward, done

        # No collision
        done = False
        return new_state, reward, done
