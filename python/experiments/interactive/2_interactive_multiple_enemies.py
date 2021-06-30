import time
from typing import Optional

import glfw
import numpy as np

from environments import VariablePendulumEnv
from environments.pendulum.state import create_variable
from evaluators.direct_actor import NOP, SWITCH
from rendering import RenderingContext
from shared_parameters import bob_radius, max_angle, connector_length, vertical_speed, \
    current_angle, position, angular_speed, enemy_radius, enemy_x

env = VariablePendulumEnv(3)
x = enemy_x
start_state: Optional[np.ndarray] = None
state: Optional[np.ndarray] = None

enemies = np.array([0, 0.25, 0.25, 0.25, 0.5, 0.25], dtype=np.float32)


def update_enemies():
    global start_state, state
    start_state = create_variable(bob_radius, max_angle, connector_length, vertical_speed, current_angle, position,
                                  angular_speed, enemy_radius, enemies)
    print(enemies)
    if state is None:
        state = start_state
    else:
        state[-enemies.shape[0]:] = enemies


update_enemies()

ctx = RenderingContext.instance

done = False
state = start_state
total_reward = 0
step = 0

selected_enemy = 0

print("Press 'Q' and 'E' to select enemy")
print(f"Currently selected: {selected_enemy}")

while not ctx.is_key_held(glfw.KEY_ESCAPE):
    env.render(state)

    step += 1

    if ctx.is_key_pressed(glfw.KEY_Q):
        selected_enemy -= 1
        selected_enemy %= (enemies.shape[0] // 2)
        print(f"Currently selected: {selected_enemy}")

    elif ctx.is_key_pressed(glfw.KEY_E):
        selected_enemy += 1
        selected_enemy %= (enemies.shape[0] // 2)
        print(f"Currently seelected: {selected_enemy}")

    if ctx.is_key_pressed(glfw.KEY_LEFT):
        enemies[selected_enemy * 2] -= 0.1
        update_enemies()

    elif ctx.is_key_pressed(glfw.KEY_RIGHT):
        enemies[selected_enemy * 2] += 0.1
        update_enemies()

    if ctx.is_key_pressed(glfw.KEY_UP):
        enemies[selected_enemy * 2 + 1] += 0.1
        update_enemies()

    elif ctx.is_key_pressed(glfw.KEY_DOWN):
        enemies[selected_enemy * 2 + 1] -= 0.1
        update_enemies()

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
