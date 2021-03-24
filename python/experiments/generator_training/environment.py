from typing import Tuple

import torch

from state import State


class Environment:
    def __init__(self, enemy_x, bob_radius, max_angle, connector_length, vertical_speed,
                 enemy_y, enemy_radius, current_angle, position, angular_speed):
        self.state = State(bob_radius, max_angle, connector_length, vertical_speed,
                           enemy_x, enemy_y, enemy_radius, current_angle, position, angular_speed)

    def reset(self) -> State:
        return self.state

    def step(self, action) -> Tuple[State, float, bool]:
        switch = action == 1

        # Interpret data
        bob_radius, max_angle, connector_length, vertical_speed, \
        enemy_x, enemy_y, enemy_radius, \
        angle, position, angular_speed = self.state

        if switch:
            angular_speed = angular_speed * -1

        # Add angular movement
        angle: torch.tensor = angle + angular_speed

        if angle.abs() > max_angle:
            angle = torch.sign(angle) * (max_angle - (angle.abs() - max_angle))
            angular_speed = angular_speed * -1

        # Add vertical movement
        position: torch.tensor = position + vertical_speed

        # Combine into the new observation
        new_state = State(bob_radius, max_angle, connector_length, vertical_speed, enemy_x, enemy_y,
                          enemy_radius, angle, position, angular_speed)

        # Check collision
        bob_center_x = torch.sin(angle) * connector_length
        bob_center_y = position - torch.cos(angle) * connector_length

        reward = 1.0 if not switch else 0.9

        distance = torch.sqrt((bob_center_x - enemy_x) ** 2 + (bob_center_y - enemy_y) ** 2)

        # Collision
        if distance <= (bob_radius + enemy_radius):
            done = True
            reward = 0.0 if not switch else -0.1
            return new_state, reward, done

        # No collision
        done = False
        return new_state, reward, done
