import glfw
import matplotlib.pyplot as plt
import torch

from common.is_greater import greater_zero
from rendering import RenderingContext, Circle, Color

plt.ioff()

if __name__ == '__main__':
    with RenderingContext(800, 600) as ctx:
        radius = torch.tensor(0.125)

        bob = Circle(Color.green, radius=radius, parent=ctx.main_scene)
        enemy = Circle(Color.red, radius=radius * 0.9, parent=ctx.main_scene)

        bob_x = torch.tensor(-0.15)
        bob.transform.local_position.x = bob_x

        enemy_x = torch.tensor(0.15, requires_grad=True)
        enemy.transform.local_position.x = enemy_x


        # def check_collision():
        #     collision = ((enemy_x - bob_x).abs() - 2 * radius)
        #             # print(collision)

        def gradient_step(enemy_x, decrease):
            enemy_x = enemy_x.detach()
            enemy_x.requires_grad = True

            reward = greater_zero((enemy_x - bob_x).abs() - 1.9 * radius, torch.tensor(0.0),
                                  torch.tensor(1.0))
            reward.retain_grad()

            print(f"reward={reward.item():.2f}")

            reward.backward()

            with torch.no_grad():
                print(f"dr={str(reward.grad)} grad={enemy_x.grad.item():.2f}")
                if decrease:
                    enemy_x -= 0.01 * enemy_x.grad
                else:
                    enemy_x += 0.01 * enemy_x.grad


        while not ctx.is_key_pressed(glfw.KEY_ESCAPE):
            ctx.render_frame()

            if ctx.is_key_held(glfw.KEY_G):
                gradient_step(enemy_x, ctx.is_key_held(glfw.KEY_LEFT_SHIFT))
                # check_collision()

            if ctx.is_key_held(glfw.KEY_LEFT):
                with torch.no_grad():
                    enemy_x -= 0.01

                # check_collision()

            elif ctx.is_key_held(glfw.KEY_RIGHT):
                with torch.no_grad():
                    enemy_x += 0.01

                # check_collision()
