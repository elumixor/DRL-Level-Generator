import glfw
import matplotlib.pyplot as plt
import torch

from rendering import RenderingContext, Circle, Color

plt.ioff()

if __name__ == '__main__':
    with RenderingContext(800, 600) as ctx:
        radius = torch.tensor([0.125])

        bob = Circle(Color.green, radius=radius, parent=ctx.main_scene)
        enemy = Circle(Color.red, radius=radius * 0.9, parent=ctx.main_scene)

        bob_x = torch.tensor([-0.15])
        bob.transform.local_position.x = bob_x

        enemy_x = torch.tensor([0.15], requires_grad=True)
        enemy.transform.local_position.x = enemy_x

        state = torch.tensor([bob_x, enemy_x], requires_grad=True)


        def take_action(action):
            global state, env

            state.requires_grad = True

            bob_x, enemy_x = state

            print(bob_x, enemy_x)

            # if action == 0.0:
            #     enemy_x_next = enemy_x - 0.01
            # elif action == 1.0:
            #     enemy_x_next = enemy_x 1 0.01

            # The above, rewritten branch-less, and, thus, differentiable
            diff = (0.01) * action + (-0.01) * (1.0 - action)

            enemy_x_next = enemy_x + diff

            bob_x_next = bob_x
            print(bob_x_next, enemy_x_next)

            next_state = torch.tensor([bob_x_next, enemy_x_next], requires_grad=True)
            print(next_state)
            next_state = torch.stack([bob_x_next, enemy_x_next])
            print(next_state)

            # now we want to find derivative wrt bob_x and enemy_x
            next_state[1].backward()

            print(state.grad)

            state = next_state.detach()

            bob.transform.local_position.x, enemy.transform.local_position.x = state


        while not ctx.is_key_pressed(glfw.KEY_ESCAPE):
            ctx.render_frame()

            if ctx.is_key_held(glfw.KEY_LEFT):
                take_action(torch.tensor(0.0))

            elif ctx.is_key_held(glfw.KEY_RIGHT):
                take_action(torch.tensor(1.0))
