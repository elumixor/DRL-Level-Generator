import glfw

from environments import PendulumEnv
from environments.pendulum import State
from rendering import RenderingContext
from shared_parameters import bob_radius, max_angle, connector_length, vertical_speed, \
    current_angle, position, angular_speed, enemy_radius, enemy_x, enemy_y

env = PendulumEnv()

x = enemy_x
start_state = State(bob_radius, max_angle, connector_length, vertical_speed,
                    current_angle, position, angular_speed, enemy_radius, x, enemy_y)

ctx = RenderingContext.instance

done = False
state = start_state
total_reward = 0
step = 0

while not ctx.is_key_held(glfw.KEY_ESCAPE):
    env.render(state)
