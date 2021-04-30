import PIL
from PIL import Image

import shared_parameters as P
from environments import PendulumEnv
from environments.pendulum import State
from environments.pendulum.rendering.renderer import render_variable
from environments.pendulum.state import enemy_x as enemy_x_index, create_variable
from rendering import RenderingContext

state = State(P.bob_radius, P.max_angle, P.connector_length, P.vertical_speed, P.current_angle, P.position,
              P.angular_speed, P.enemy_radius, 0, P.enemy_y)


def render_single_enemy(enemy_x, resolution=1.0) -> PIL.Image:
    state[enemy_x_index] = enemy_x
    env = PendulumEnv()
    img = env.render(state, to_image=True, resolution=resolution)
    RenderingContext.instance.terminate()
    return img


def render_variable_enemies(enemies, resolution=1.0):
    state = create_variable(P.bob_radius, P.max_angle, P.connector_length, P.vertical_speed, P.current_angle,
                            P.position, P.angular_speed, P.enemy_radius, enemies)

    with RenderingContext(800, 600) as ctx:
        return render_variable(ctx, state, resolution)
