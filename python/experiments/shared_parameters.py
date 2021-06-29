import numpy as np

# region Environment starting state
bob_radius = 0.1
max_angle = np.deg2rad(50)
connector_length = 0.3
vertical_speed = 0.01
current_angle = 0
position = 0
angular_speed = 0.05
enemy_radius = 0.1
enemy_x = 0.1
enemy_y = 0.25
# endregion

enemy_x_min = -1
enemy_x_max = 1
enemy_y_min = -1
enemy_y_max = 1

subdivisions = 100
epochs = 100000

num_actors = 50
num_evaluations = 50
max_trajectory_length = 75


class skill_weighting:
    mean = 0.75
    std = 0.25
    skew = 2
