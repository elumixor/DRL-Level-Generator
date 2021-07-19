import time

import glfw
import torch

from evaluators.direct_actor import NOP, SWITCH
from framework.environments import PendulumEnvironment, PendulumRenderer
from rendering import RenderingContext
from shared_parameters import *

env = PendulumEnvironment(bob_radius, max_angle, connector_length, vertical_speed, angular_speed, enemy_radius,
                          enemy_x_min, enemy_x_max, enemy_y)
renderer = PendulumRenderer(bob_radius, connector_length, enemy_radius, enemy_y)

x = enemy_x
start_state = env.get_starting_state()

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
        state.set_enemy_x(0, x)
        start_state.set_enemy_x(0, x)

    if ctx.is_key_pressed(glfw.KEY_RIGHT):
        x += 0.1
        state.set_enemy_x(0, x)
        start_state.set_enemy_x(0, x)

    if ctx.is_key_pressed(glfw.KEY_SPACE):
        state, reward, done = env.transition(state, torch.tensor(SWITCH))

    else:
        time.sleep(0.016)
        state, reward, done = env.transition(state, torch.tensor(NOP))

    total_reward += reward

    if step >= 100:
        done = True

    if done or ctx.is_key_pressed(glfw.KEY_R):
        print(f"Done after {step} steps. Total reward = {total_reward}")

        done = False
        state = start_state
        total_reward = 0
        step = 0
