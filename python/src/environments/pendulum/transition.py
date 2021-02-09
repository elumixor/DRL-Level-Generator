from typing import Tuple, List

import torch

from .enemy import EnemyDynamicConfiguration, EnemyStaticConfiguration
from .pendulum import PendulumDynamicConfiguration, PendulumStaticConfiguration

max_enemies = 1
state_size = PendulumDynamicConfiguration.size + 1 + max_enemies * EnemyDynamicConfiguration.size
observation_size = state_size
action_size = 2

static_size = PendulumStaticConfiguration.size + 1 + max_enemies * EnemyStaticConfiguration.size
parameters_size = state_size + static_size


def transition(state: torch.tensor, action: torch.tensor,
               static_configuration: torch.tensor) -> Tuple[torch.tensor, float, bool]:
    switch = action == 1

    # Interpret data
    angle, position, angular_speed = state[:PendulumDynamicConfiguration.size]
    enemies_count = int(state[PendulumDynamicConfiguration.size])

    bob_radius, max_angle, connector_length, vertical_speed = static_configuration[:PendulumStaticConfiguration.size]

    enemies_configurations = static_configuration[PendulumStaticConfiguration.size + 1:]

    if switch:
        angular_speed = angular_speed * -1

    # Add angular movement
    angle: torch.tensor = angle + angular_speed

    if angle.abs() > max_angle:
        angle = torch.sign(angle) * (max_angle - (angle.abs() - max_angle))
        angular_speed = angular_speed * -1

    # Add vertical movement
    position: torch.tensor = position + vertical_speed

    # Combine into the new state
    new_state = torch.tensor([angle, position, angular_speed, enemies_count])

    # Check collision
    bob_center_x = torch.sin(angle) * connector_length
    bob_center_y = position - torch.cos(angle) * connector_length

    reward = 1.0 if not switch else 0.99

    for i in range(enemies_count):
        enemy = enemies_configurations[i * EnemyStaticConfiguration.size:(i + 1) * EnemyStaticConfiguration.size]
        enemy_radius, enemy_x, enemy_y = enemy

        distance = torch.sqrt((bob_center_x - enemy_x) ** 2 + (bob_center_y - enemy_y) ** 2)

        # Collision
        if distance <= (bob_radius + enemy_radius):
            done = True
            reward = 0.0 if not switch else -0.01
            return new_state, reward, done

    # No collision
    done = False
    return new_state, reward, done


def configurations2parameters(pendulum_static_configuration: PendulumStaticConfiguration,
                              enemies_static_configurations: List[EnemyStaticConfiguration],
                              pendulum_dynamic_configuration: PendulumDynamicConfiguration,
                              enemies_dynamic_configurations: List[EnemyDynamicConfiguration]) -> torch.tensor:
    return torch.tensor([
        *pendulum_static_configuration,
        len(enemies_static_configurations),
        *[value for configuration in enemies_static_configurations for value in configuration],

        *pendulum_dynamic_configuration,
        len(enemies_dynamic_configurations),
        *[value for configuration in enemies_dynamic_configurations for value in configuration]
    ], dtype=torch.float32)


def interpret_generated_parameters(generated_parameters: torch.tensor) -> Tuple[torch.tensor, torch.tensor]:
    """
    Splits the tensor from the generator into the static parameters and a starting state
    :returns: A tensor of the static parameters and a tensor of the starting state
    """
    return torch.split(generated_parameters, [static_size, state_size])


def interpret_static_configuration(configuration: torch.tensor) -> Tuple[PendulumStaticConfiguration,
                                                                         List[EnemyStaticConfiguration]]:
    """
    Creates human-readable configuration objects from the static configuration tensor
    """
    pendulum_size = PendulumStaticConfiguration.size
    enemy_size = EnemyStaticConfiguration.size

    pendulum_configuration = PendulumStaticConfiguration(*configuration[:pendulum_size].tolist())
    enemies_count = int(configuration[pendulum_size])

    slices = [configuration[pendulum_size + 1 + i * enemy_size:pendulum_size + 1 + (i + 1) * enemy_size]
              for i in range(enemies_count)]

    enemies_configurations = [EnemyStaticConfiguration(*s.tolist()) for s in slices]

    return pendulum_configuration, enemies_configurations


def interpret_state(state: torch.tensor) -> Tuple[PendulumDynamicConfiguration,
                                                  List[EnemyDynamicConfiguration]]:
    """
    Creates human-readable configuration objects from the state tensor
    """
    pendulum_size = PendulumDynamicConfiguration.size
    enemy_size = EnemyDynamicConfiguration.size

    pendulum_configuration = PendulumDynamicConfiguration(*state[:pendulum_size].tolist())

    enemies_count = int(state[pendulum_size])
    enemies_configurations = [EnemyDynamicConfiguration()] * enemies_count

    return pendulum_configuration, enemies_configurations
