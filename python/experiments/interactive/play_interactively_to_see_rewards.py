import time

import glfw

from environments import PendulumEnv
from environments.pendulum import State
from evaluators.direct_actor import NOP, SWITCH
from rendering import RenderingContext
from shared_parameters import bob_radius, max_angle, connector_length, vertical_speed, \
    current_angle, position, angular_speed, enemy_radius, enemy_x, enemy_y

env = PendulumEnv()
start_state = State(bob_radius, max_angle, connector_length, vertical_speed,
                    current_angle, position, angular_speed, enemy_radius, enemy_x, enemy_y)

ctx = RenderingContext.instance

done = False
state = start_state
total_reward = 0
step = 0

while not ctx.is_key_held(glfw.KEY_ESCAPE):
    env.render(state)
    step += 1

    if ctx.is_key_pressed(glfw.KEY_SPACE):
        state, reward, done = env.transition(state, SWITCH)

    else:
        time.sleep(0.016)
        state, reward, done = env.transition(state, NOP)

    total_reward += reward

    if step >= 100:
        done = True

    if done or ctx.is_key_pressed(glfw.KEY_R):
        print(f"Done after {step} steps. Total reward = {total_reward}")

        done = False
        state = start_state
        total_reward = 0
        step = 0
