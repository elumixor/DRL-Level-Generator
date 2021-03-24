import torch

from common import tensored


@tensored
class State(torch.Tensor):
    # Define init for static code checking
    def __init__(self, bob_radius, max_angle, connector_length, vertical_speed,
                 enemy_x, enemy_y, enemy_radius, current_angle, position, angular_speed):
        ...

    # Define fields for access
    bob_radius: torch.Tensor
    max_angle: torch.Tensor
    connector_length: torch.Tensor
    vertical_speed: torch.Tensor

    enemy_x: torch.Tensor
    enemy_y: torch.Tensor
    enemy_radius: torch.Tensor

    current_angle: torch.Tensor
    position: torch.Tensor
    angular_speed: torch.Tensor
