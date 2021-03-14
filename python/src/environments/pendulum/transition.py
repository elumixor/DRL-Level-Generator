from typing import Tuple

import torch

from .state import PendulumState


def transition(state: PendulumState, action: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, bool]:
    """
    We need

    d(s_{t+1})    d(r_t)
    ----------    ------
      d(s_t)      d(s_t)

    :param state:
    :param action:
    :return:
    """

    switch = action == 1

    # Interpret data
    bob_radius, max_angle, connector_length, vertical_speed, \
    enemy_x, enemy_y, enemy_radius, \
    angle, position, angular_speed = state

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
    new_state = PendulumState(bob_radius, max_angle, connector_length, vertical_speed, enemy_x, enemy_y, enemy_radius,
                              angle, position, angular_speed)

    # Check collision
    bob_center_x = torch.sin(angle) * connector_length

    # Collision
    collision = distance <= 0.0

    # base_reward = greater_zero(distance, torch.tensor(1.0), torch.tensor(0.0))
    #
    # reward = base_reward - (0.0 if not switch else 0.1)
    reward = torch.tensor(1.0)

    return new_state, reward, collision
