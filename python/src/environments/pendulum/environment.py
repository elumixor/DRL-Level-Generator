from typing import Tuple

import numpy as np
from numba import njit, typed, types, typeof, int32
from numba.experimental import jitclass

from utils import vec
from .rendering import PendulumRenderer
from .state import create as State
from ..base_env import BaseEnv
from ..spaces import DiscreteSpace, BoxSpace, DiscreteSpaceJIT, BoxSpaceJIT


@njit
def transition(state: np.ndarray, action: int):
    switch = action == 1

    # Interpret data
    bob_radius, max_angle, connector_length, vertical_speed, angle, position, angular_speed, enemy_radius, \
    enemy_x, enemy_y = state

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
    new_state[5] = angle
    new_state[6] = position
    new_state[7] = angular_speed

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

        low = State(0.05, 0, 0.05, 0.1, -1, -1, 0.05, 0, 0, 0)
        high = State(1, 90, 1, 1, 1, 1, 1, 90, 1, 90)

        self._state_space = BoxSpace(low, high)
        self._action_space = DiscreteSpace(2)

    @property
    def state_space(self) -> BoxSpace:
        return self._state_space

    @property
    def action_space(self) -> DiscreteSpace:
        return self._action_space

    def transition(self, state: vec, action: vec) -> Tuple[vec, float, bool]:
        return transition(state, action)


@jitclass([
    ("_state_space", types.ListType(typeof(BoxSpaceJIT(np.zeros(2, dtype=np.float32), np.zeros(2, dtype=np.float32))))),
    ("_action_space", types.ListType(typeof(DiscreteSpaceJIT(2))))
])
class PendulumEnvJIT:
    def __init__(self):
        low = State(0.05, 0, 0.05, 0.1, -1, -1, 0.05, 0, 0, 0)
        high = State(1, 90, 1, 1, 1, 1, 1, 90, 1, 90)

        self._state_space = typed.List([BoxSpaceJIT(low, high)])
        self._action_space = typed.List([DiscreteSpaceJIT(2)])

    @property
    def state_space(self):
        return self._state_space[0]

    @property
    def action_space(self):
        return self._action_space[0]

    def transition(self, state: vec, action: vec) -> Tuple[vec, float, bool]:
        return transition(state, action)


@jitclass([("num_enemies", int32)])
class VariablePendulumJIT:
    def __init__(self, num_enemies: int):
        self.num_enemies = num_enemies

    def transition(self, state: vec, action: vec) -> Tuple[vec, float, bool]:
        switch = action == 1

        # Interpret data
        bob_radius, max_angle, connector_length, vertical_speed, angle, position, angular_speed, enemy_radius = \
            state[:8]

        # x and y per enemy
        enemies = state[8:8 + self.num_enemies * 2]

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
        new_state[5] = angle
        new_state[6] = position
        new_state[7] = angular_speed

        # Check collision
        bob_center_x = np.sin(angle) * connector_length
        bob_center_y = position - np.cos(angle) * connector_length

        for i in range(self.num_enemies):
            enemy_x, enemy_y = enemies[2 * i], enemies[2 * i + 1]
            distance = np.sqrt((bob_center_x - enemy_x) ** 2 + (bob_center_y - enemy_y) ** 2)
            collision = distance <= (bob_radius + enemy_radius)

            if collision:
                return new_state, (0.0 if not switch else -0.1), True

        # No collision
        return new_state, (1.0 if not switch else 0.9), False
