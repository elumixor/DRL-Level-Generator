import numpy as np

# region Environment starting state
bob_radius = 0.1
max_angle = float(np.deg2rad(50))
connector_length = 0.4
vertical_speed = 0.01
current_angle = 0
position = 0
angular_speed = 0.05
enemy_radius = 0.1
enemy_x = 0.1
enemy_y = 0.25
enemy_y_1 = 0.65
# endregion

enemy_x_min = -0.5
enemy_x_max = 0.5
enemy_y_min = 0.15
enemy_y_max = 0.8

subdivisions = 100
epochs = 100000

num_actors = 50
num_evaluations = 50
max_trajectory_length = 100
max_trajectory_length_1 = 150


class skill_weighting:
    mean = 0.75
    std = 0.25
    skew = 2


pendulum_env_args = bob_radius, max_angle, connector_length, vertical_speed, angular_speed, enemy_radius, enemy_x_min, \
                    enemy_x_max, enemy_y
