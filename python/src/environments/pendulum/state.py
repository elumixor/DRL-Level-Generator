import numpy as np
from numba import njit


# noinspection PyShadowingNames
@njit
def create(bob_radius, max_angle, connector_length, vertical_speed, current_angle, position, angular_speed,
           enemy_radius, enemy_x, enemy_y):
    return np.array([bob_radius, max_angle, connector_length, vertical_speed, current_angle, position, angular_speed,
                     enemy_radius, enemy_x, enemy_y], dtype=np.float32)


@njit
def create_variable(bob_radius, max_angle, connector_length, vertical_speed, current_angle, position, angular_speed,
                    enemy_radius, enemies):
    return np.concatenate(
        (np.array((bob_radius, max_angle, connector_length, vertical_speed, current_angle, position, angular_speed,
                   enemy_radius), dtype=np.float32), enemies), axis=-1)


bob_radius = 0
max_angle = 1
connector_length = 2
vertical_speed = 3
current_angle = 4
position = 5
angular_speed = 6

enemy_radius = 7

enemy_x = 8
enemy_y = 9

size = 10

size_fixed = enemy_radius + 1
