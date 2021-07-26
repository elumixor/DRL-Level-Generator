import time

import glfw

from pendulum import PendulumEnvironment, PendulumRenderer
from pendulum.actions import NOP, SWITCH
from rendering import RenderingContext
from shared_parameters import *

delta_time = 5
env = PendulumEnvironment(bob_radius, max_angle, connector_length, vertical_speed, angular_speed, enemy_radius,
                          enemy_x_min, enemy_x_max, enemy_y, enemy_y_1, enemy_y_2, time_scale=delta_time)
renderer = PendulumRenderer(bob_radius, connector_length, enemy_radius, enemy_y, enemy_y_1, enemy_y_2)

start_state = env.get_starting_state()
enemy_x = start_state.enemy_x

ctx = RenderingContext.instance

done = False
state = start_state

total_reward = 0
step = 0

i = 0


def update_selected(delta):
    enemy_x[i] += delta


def update_state():
    global state
    state.enemy_x = enemy_x
    start_state.enemy_x = enemy_x


while not ctx.is_key_held(glfw.KEY_ESCAPE):
    renderer.render(state)

    step += 1

    if ctx.is_key_pressed(glfw.KEY_LEFT):
        update_selected(-0.1)
        update_state()

    if ctx.is_key_pressed(glfw.KEY_RIGHT):
        update_selected(0.1)
        update_state()

    if ctx.is_key_pressed(glfw.KEY_UP):
        i += 1
        i %= enemy_x.shape[0]

    if ctx.is_key_pressed(glfw.KEY_DOWN):
        i -= 1
        i %= enemy_x.shape[0]

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

    if step >= max_trajectory_length_2 / delta_time:
        done = True

    if done or ctx.is_key_pressed(glfw.KEY_R):
        print(f"Done after {step} steps. Total reward = {total_reward}")

        done = False
        state = start_state
        total_reward = 0
        step = 0
