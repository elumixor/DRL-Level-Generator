from typing import Tuple

import numpy as np
from numba import njit

from utils import vec
from .rendering import PendulumRenderer
from .state import create as State, size as state_size
from ..base_env import BaseEnv
from ..spaces import DiscreteSpace, BoxSpace


@njit
def transition(state: np.ndarray, action: int):
    switch = action == 1

    # Interpret data
    bob_radius, max_angle, connector_length, vertical_speed, \
    enemy_x, enemy_y, enemy_radius, \
    angle, position, angular_speed = state

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
    new_state = State(bob_radius, max_angle, connector_length, vertical_speed, enemy_x, enemy_y,
                      enemy_radius, angle, position, angular_speed)

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


class PendulumEnv(BaseEnv[vec, vec]):
    def __init__(self):
        super().__init__(PendulumRenderer)

        low = np.zeros(state_size, dtype=np.float32)
        high = np.ones_like(low, dtype=np.float32)

        self._state_space = BoxSpace(low, high)
        self._action_space = DiscreteSpace(2)

    @property
    def state_space(self) -> BoxSpace:
        return self._state_space

    @property
    def action_space(self) -> DiscreteSpace:
        return self._action_space

    def transition(self, state: vec, action: vec) -> Tuple[vec, float, bool]:
        print("transition", state, action)
        return transition(state, action)
