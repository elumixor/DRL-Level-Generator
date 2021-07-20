from random import random

import torch

from framework import AbstractAgent
from pendulum import PendulumState
from ..actions import NOP, SWITCH


class HeuristicPendulumActor(AbstractAgent):
    def __init__(self, enemy_radius: float, bob_radius: float, connector_length: float, *enemies_y: float,
                 skill: float = 1.0, action_distance: float = 0.1):
        self.enemy_radius = enemy_radius
        self.bob_radius = bob_radius
        self.connector_length = connector_length
        self.enemies_y = enemies_y

        self.action_distance = action_distance
        self.randomness = 1 - skill
        self.num_enemies = len(self.enemies_y)

    @property
    def random_action(self):
        return NOP if random() > 0.5 else SWITCH

    def get_action(self, state: PendulumState) -> int:
        if random() < self.randomness:
            return self.random_action

        y = state.vertical_position
        angle = state.current_angle

        bob = torch.tensor([angle.sin() * self.connector_length, y - angle.cos() * self.connector_length])

        enemies = torch.tensor([[x, y] for x, y in zip(state.enemy_x, self.enemies_y)])
        distances = torch.norm(enemies - bob, dim=-1) - (self.bob_radius + self.enemy_radius)

        min_dist, min_dist_i = distances.min(dim=-1)

        if min_dist > self.action_distance:
            return NOP

        angle_next = angle + state.angular_speed

        bob_next = torch.tensor(
            [(angle_next.sin() * self.connector_length), (y - angle_next.cos() * self.connector_length)])

        closest = enemies[min_dist_i]
        distance_next = torch.norm(bob_next - closest)

        return NOP if distance_next > min_dist else SWITCH
