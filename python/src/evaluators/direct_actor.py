import random
from typing import Optional

import numpy as np
import torch
from numba import float32, int32
from numba.experimental import jitclass

from environments.pendulum.state import connector_length, bob_radius, position, enemy_radius, enemy_x, enemy_y, \
    current_angle, angular_speed

NOP = 0
SWITCH = 1


@jitclass([
    ("action_distance", float32),
    ("randomness", float32),
])
class DirectActor:
    def __init__(self, skill, action_distance: Optional[torch.Tensor] = None):
        if action_distance is None:
            action_distance = 0.1

        self.action_distance = action_distance
        self.randomness = 1 - skill

    def get_action(self, state: np.ndarray) -> int:
        if random.random() < self.randomness:
            return NOP if random.random() > 0.5 else SWITCH

        y = state[position]
        cl = state[connector_length]

        r_bob = state[bob_radius]
        r_enemy = state[enemy_radius]

        e_x, e_y = state[enemy_x], state[enemy_y]

        angle = state[current_angle]
        a_s = state[angular_speed]

        bob_current_x = np.sin(angle) * cl
        bob_current_y = y - np.cos(angle) * cl

        distance = np.sqrt((bob_current_x - e_x) ** 2 + (bob_current_y - e_y) ** 2)
        if distance - r_bob - r_enemy > self.action_distance:
            return NOP

        next_angle = angle + a_s

        bob_next_x = np.sin(next_angle) * cl
        bob_next_y = y - np.cos(next_angle) * cl

        distance_next = np.sqrt((bob_next_x - e_x) ** 2 + (bob_next_y - e_y) ** 2)
        return NOP if distance_next > distance else SWITCH


@jitclass([
    ("action_distance", float32),
    ("randomness", float32),
    ("num_enemies", int32),
])
class ActorVariable:
    def __init__(self, skill, action_distance: Optional[torch.Tensor] = None):
        if action_distance is None:
            action_distance = 0.1

        self.action_distance = action_distance
        self.randomness = 1 - skill
        self.num_enemies = 3

    def get_action(self, state: np.ndarray) -> int:
        if random.random() < self.randomness:
            return NOP if random.random() > 0.5 else SWITCH

        y = state[position]
        cl = state[connector_length]

        r_bob = state[bob_radius]
        r_enemy = state[enemy_radius]

        angle = state[current_angle]
        a_s = state[angular_speed]

        bob_current_x = np.sin(angle) * cl
        bob_current_y = y - np.cos(angle) * cl

        enemies = state[8:8 + self.num_enemies * 2]
        distances = np.zeros(self.num_enemies, dtype=np.float32)

        for i in range(self.num_enemies):
            enemy_x, enemy_y = enemies[2 * i], enemies[2 * i + 1]
            distances[i] = np.sqrt((bob_current_x - enemy_x) ** 2 + (bob_current_y - enemy_y) ** 2) - r_bob - r_enemy

        min_dist_i = distances.argmin()
        min_dist = distances[min_dist_i]

        if min_dist > self.action_distance:
            return NOP

        next_angle = angle + a_s

        bob_next_x = np.sin(next_angle) * cl
        bob_next_y = y - np.cos(next_angle) * cl

        enemy_x, enemy_y = enemies[2 * min_dist_i], enemies[2 * min_dist_i + 1]
        distance_next = np.sqrt((bob_next_x - enemy_x) ** 2 + (bob_next_y - enemy_y) ** 2)

        return NOP if distance_next > min_dist else SWITCH
