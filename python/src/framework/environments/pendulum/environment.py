from random import random
from typing import Tuple

import torch
from torch import Tensor

from utils import sign
from .state import PendulumState
from ..abstract_environment import AbstractEnvironment


class PendulumEnvironment(AbstractEnvironment):
    """
    Pendulum environment.

    - Delta time is for the change between frames

    Things that do not change are provided in __init__:
    - Bob radius
    - Connector length
    - Vertical speed
    - Maximum angle
    - Angular speed
    - Enemy radius
    - Enemy x_min
    - Enemy x_max
    - Enemies' y (implicitly also sets the number of enemies)

    Things that are getting randomized on every new state
    - Enemies' x (from enemy x_min to enemy x_max)
    - Current angle (from minus maximum angle to maximum angle)
    - Angular speed (changes direction, but not magnitude)

    Things that change with time
    - Vertical position
    - Angular speed (changes direction, but not magnitude)
    - Current angle (changes direction, but not magnitude)

    """

    def __init__(self, bob_radius: float, max_angle: float, connector_length: float,
                 vertical_speed: float, angular_speed: float, enemy_radius: float, enemy_x_min: float,
                 enemy_x_max: float, *enemies_y: float, time_scale: float = 1, step_reward: float = 0.0,
                 action_reward: float = 0.0, death_reward: float = 0.0):
        self.time_scale = time_scale

        self.bob_radius = bob_radius
        self.max_angle = max_angle
        self.connector_length = connector_length
        self.vertical_speed = vertical_speed
        self.angular_speed = angular_speed
        self.enemy_radius = enemy_radius
        self.enemy_x_min = enemy_x_min
        self.enemy_x_max = enemy_x_max
        self.enemies_y = enemies_y

        self.num_enemies = len(self.enemies_y)
        self.enemy_x_diff = self.enemy_x_max - self.enemy_x_min
        self.collision_distance = self.bob_radius + self.enemy_radius

        self.step_reward = step_reward
        self.action_reward = action_reward
        self.death_reward = death_reward

    def get_starting_state(self) -> PendulumState:
        """
        Returns a randomized starting state
        :return: Tensor: [current_angle, angular_speed, vertical_position, enemy_0_x, enemy_1_x, ..., enemy_i_x]
        """
        # Randomize enemy positions for each enemy
        enemies_x = [random() * self.enemy_x_diff + self.enemy_x_min for _ in range(self.num_enemies)]

        # Also randomize current angle
        current_angle = (random() * 2 - 1) * self.max_angle

        # Assign random direction to the angular speed
        angular_speed = sign(self.angular_speed)

        # Starting vertical position is going to always be zero
        vertical_position = 0.0

        return PendulumState.create(current_angle, angular_speed, vertical_position, *enemies_x)

    def transition(self, state: Tensor, action: int) -> Tuple[PendulumState, float, bool]:
        current_angle, angular_speed, vertical_position, *enemies_x = state
        switch = action == 1

        if switch:
            angular_speed = angular_speed * -1

        reward = self.action_reward if switch else 0.0

        # Add angular movement
        current_angle = current_angle + angular_speed * self.time_scale

        if current_angle.abs() > self.max_angle:
            current_angle = current_angle.sign() * (self.max_angle - (current_angle.abs() - self.max_angle))
            angular_speed *= -1

        # Add vertical movement
        vertical_position = vertical_position + self.vertical_speed * self.time_scale

        # Combine into the new observation
        new_state = PendulumState.create(current_angle, angular_speed, vertical_position, *enemies_x)

        # Check collision
        bob_x = torch.sin(current_angle) * self.connector_length
        bob_y = vertical_position - torch.cos(current_angle) * self.connector_length
        bob_position = torch.tensor([bob_x, bob_y])

        for enemy_x, enemy_y in zip(enemies_x, self.enemies_y):
            enemy_position = torch.tensor([enemy_x, enemy_y])
            distance = torch.norm(bob_position - enemy_position)
            collision = distance <= self.collision_distance

            if collision:
                return new_state, reward + self.death_reward, True

        # No collision
        return new_state, reward + self.step_reward, False
