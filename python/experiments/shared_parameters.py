import numpy as np

connector_length = 0.5
max_angle = 30
enemy_radius = 0.1
bob_radius = 0.15

enemy_x_min = -1
enemy_x_max = 1

enemy_y_min = -1
enemy_y_max = 1

subdivisions = 100
vertical_speed = 0.1
angular_speed = -15
enemy_y = 0
position = 0
epochs = 100000

num_actors = 50
num_evaluations = 50
max_trajectory_length = 75

current_angle = max_angle


class skill_weighting:
    mean = 0.75
    std = 0.25
    skew = 2


max_angle = np.deg2rad(max_angle)
current_angle = np.deg2rad(current_angle)
