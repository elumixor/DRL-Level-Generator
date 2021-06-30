from typing import Tuple

import numpy as np
from numba import int32, njit
from numba.experimental import jitclass

from environments.base_env import BaseEnv
from environments.pendulum.rendering import VariablePendulumRenderer
from environments.pendulum.state import current_angle as s_current_angle, position as s_position, \
    angular_speed as s_angular_speed
from environments.spaces import Space
from utils import vec


@njit
def transition(num_enemies: int, state: np.ndarray, action: np.ndarray) -> Tuple[vec, float, bool]:
    switch = action == 1

    # Interpret data
    bob_radius, max_angle, connector_length, vertical_speed, angle, position, angular_speed, enemy_radius = \
        state[:8]

    # x and y per enemy
    enemies = state[8:8 + num_enemies * 2]

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
    new_state = state.copy()
    new_state[s_current_angle] = angle
    new_state[s_position] = position
    new_state[s_angular_speed] = angular_speed

    # Check collision
    bob_center_x = np.sin(angle) * connector_length
    bob_center_y = position - np.cos(angle) * connector_length

    for i in range(num_enemies):
        enemy_x, enemy_y = enemies[2 * i], enemies[2 * i + 1]
        distance = np.sqrt((bob_center_x - enemy_x) ** 2 + (bob_center_y - enemy_y) ** 2)
        collision = distance <= (bob_radius + enemy_radius)

        if collision:
            return new_state, (0.0 if not switch else -0.1), True

    # No collision
    return new_state, (1.0 if not switch else 0.9), False


class VariablePendulumEnv(BaseEnv[vec, vec]):
    @property
    def state_space(self) -> Space:
        pass

    @property
    def action_space(self) -> Space:
        pass

    def __init__(self, num_enemies: int):
        super().__init__(VariablePendulumRenderer)
        self.num_enemies = num_enemies

    def transition(self, state: vec, action: vec) -> Tuple[vec, float, bool]:
        return transition(self.num_enemies, state, action)


@jitclass([("num_enemies", int32)])
class VariablePendulumEnvJIT:
    def __init__(self, num_enemies: int):
        self.num_enemies = num_enemies

    def transition(self, state: vec, action: vec) -> Tuple[vec, float, bool]:
        return transition(self.num_enemies, state, action)
