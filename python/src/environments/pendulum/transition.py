from typing import Tuple, List

import torch

from .enemy import EnemyDynamicConfiguration, EnemyStaticConfiguration
from .pendulum import PendulumDynamicConfiguration, PendulumStaticConfiguration

max_enemies = 1
state_size = PendulumDynamicConfiguration.size + 1 + max_enemies * EnemyDynamicConfiguration.size
observation_size = 0
action_size = 0

static_size = PendulumStaticConfiguration.size + 1 + max_enemies * EnemyStaticConfiguration.size
parameters_size = state_size + static_size


def transition(state: torch.tensor, action: torch.tensor,
               static_configuration: torch.tensor) -> Tuple[torch.tensor, float, bool]:
    ...


def interpretation2state(pendulum_configuration: PendulumDynamicConfiguration,
                         enemies_configurations: List[EnemyDynamicConfiguration]) -> torch.tensor:
    ...


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
