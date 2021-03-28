import numpy as np
from numba import njit


@njit
def create(bob_radius, max_angle, connector_length, vertical_speed, enemy_x, enemy_y, enemy_radius, current_angle,
           position, angular_speed) -> np.ndarray:
    return np.array([bob_radius, max_angle, connector_length, vertical_speed, enemy_x, enemy_y, enemy_radius,
                     current_angle, position, angular_speed], dtype=np.float32)


bob_radius = 0
max_angle = 1
connector_length = 2
vertical_speed = 3

enemy_x = 4
enemy_y = 5
enemy_radius = 6

current_angle = 7
position = 8
angular_speed = 9
