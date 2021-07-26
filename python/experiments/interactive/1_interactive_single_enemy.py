import time

import glfw

from pendulum import PendulumEnvironment, PendulumRenderer
from pendulum.actions import NOP, SWITCH
from rendering import RenderingContext
from shared_parameters import *

delta_time = 1
env = PendulumEnvironment(bob_radius, max_angle, connector_length, vertical_speed, angular_speed, enemy_radius,
                          enemy_x_min, enemy_x_max, enemy_y, time_scale=delta_time)
renderer = PendulumRenderer(bob_radius, connector_length, enemy_radius, enemy_y)

start_state = env.get_starting_state()
x = start_state.enemy_x

ctx = RenderingContext.instance

done = False
state = start_state

total_reward = 0
step = 0

while not ctx.is_key_held(glfw.KEY_ESCAPE):
    renderer.render(state)

    step += 1

    if ctx.is_key_pressed(glfw.KEY_LEFT):
        x -= 0.1
        state.enemy_x = x
        start_state.enemy_x = x

    if ctx.is_key_pressed(glfw.KEY_RIGHT):
        x += 0.1
        state.enemy_x = x
        start_state.enemy_x = x

    # F - Faster
    if ctx.is_key_pressed(glfw.KEY_F):
        delta_time *= 2
        env.time_scale = delta_time

    # S - Slower
    if ctx.is_key_pressed(glfw.KEY_S):
        delta_time /= 2
        env.time_scale = delta_time

    if ctx.is_key_pressed(glfw.KEY_SPACE):
        state, reward, done = env.transition(state, SWITCH)

    else:
        time.sleep(0.016 * delta_time)
        state, reward, done = env.transition(state, NOP)

    total_reward += reward

    if step >= max_trajectory_length / delta_time:
        done = True

    if done or ctx.is_key_pressed(glfw.KEY_R):
        print(f"Done after {step} steps. Total reward = {total_reward}")

        done = False
        state = start_state
        total_reward = 0
        step = 0
