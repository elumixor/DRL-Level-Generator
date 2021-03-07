import time

from environments.pendulum import PendulumEnvironment
from environments.pendulum.generators.draggable import DraggableGenerator
from rendering import RenderingContext

if __name__ == '__main__':
    with RenderingContext(800, 600) as ctx:
        generator = DraggableGenerator(ctx)
        trajectories = 1_000

        with PendulumEnvironment(ctx, generator, difficulty=0.5) as env:
            env.reset()
            env.render()
            texture = ctx.renderTexture(resolution=2)
            time.sleep(1)
            texture.save("text.png")
