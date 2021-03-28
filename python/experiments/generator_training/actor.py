import random
from typing import Optional

import numpy as np
import torch
from numba import float32
from numba.experimental import jitclass

import state as State
from utilities import time_section

NOP = 0
SWITCH = 1


@jitclass([
    ("action_distance", float32),
    ("randomness", float32),
])
class Actor:
    def __init__(self, skill, action_distance: Optional[torch.Tensor] = None):
        if action_distance is None:
            action_distance = 0.1

        self.action_distance = action_distance
        self.randomness = skill

    def get_action(self, state: np.ndarray) -> int:
        if random.random() < self.randomness:
            return NOP if random.random() > 0.5 else SWITCH

        y = state[State.position]
        connector_length = state[State.connector_length]

        r_bob = state[State.bob_radius]
        r_enemy = state[State.enemy_radius]

        enemy_x, enemy_y = state[State.enemy_x], state[State.enemy_y]

        angle = state[State.current_angle]
        angular_speed = state[State.angular_speed]

        bob_current_x = np.sin(angle) * connector_length
        bob_current_y = y - np.cos(angle) * connector_length

        distance = np.sqrt((bob_current_x - enemy_x) ** 2 + (bob_current_y - enemy_y) ** 2)
        if distance - r_bob - r_enemy > self.action_distance:
            return NOP

        next_angle = angle + angular_speed

        bob_next_x = np.sin(next_angle) * connector_length
        bob_next_y = y - np.cos(next_angle) * connector_length

        distance_next = np.sqrt((bob_next_x - enemy_x) ** 2 + (bob_next_y - enemy_y) ** 2)
        return NOP if distance_next > distance else SWITCH


if __name__ == '__main__':
    actor = Actor(..., 0.3, 0.5)
    state = State.create(0.25, np.deg2rad(30), 0.2, 0.1, 0.3, 0.5, 0.15, np.deg2rad(30), 0, -0.1)

    with time_section():
        for _ in range(10_000_000):
            action = actor.get_action(state)
