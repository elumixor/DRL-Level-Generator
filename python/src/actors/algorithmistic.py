import random
from typing import Optional

import torch

from core import Actor


class AlgorithmicActor(Actor):
    def __init__(self, env, action_distance: Optional[torch.Tensor] = None):
        super.__init__(env)
        if action_distance is None:
            action_distance = torch.tensor(0.1)

        self.action_distance = action_distance
        self.randomness = torch.tensor([0.0])

    def get_action(self, observation: PendulumState) -> torch.Tensor:
        if self.randomness > 0 and random.random() < self.randomness:
            return ACTION_NOP if random.random() > 0.5 else ACTION_SWITCH

        y = observation.position
        connector_length = observation.connector_length

        r_bob = observation.bob_radius
        r_enemy = observation.enemy_radius

        enemy_x, enemy_y = observation.enemy_x, observation.enemy_y

        angle = observation.current_angle
        angular_speed = observation.angular_speed

        bob_current_x = torch.sin(angle) * connector_length
        bob_current_y = y - torch.cos(angle) * connector_length

        distance = torch.sqrt((bob_current_x - enemy_x) ** 2 + (bob_current_y - enemy_y) ** 2)
        if distance - r_bob - r_enemy > self.action_distance:
            return ACTION_NOP

        next_angle = angle + angular_speed

        bob_next_x = torch.sin(next_angle) * connector_length
        bob_next_y = y - torch.cos(next_angle) * connector_length

        distance_next = torch.sqrt((bob_next_x - enemy_x) ** 2 + (bob_next_y - enemy_y) ** 2)
        return ACTION_NOP if distance_next > distance else ACTION_SWITCH
