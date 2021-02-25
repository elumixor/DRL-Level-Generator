import time

from environments.pendulum import PendulumEnvironment
from environments.pendulum.generators.draggable import DraggableGenerator
from environments.pendulum.heuristics import HeuristicsPlayer
from rendering import RenderingContext

if __name__ == '__main__':
    with RenderingContext(800, 600) as ctx:
        generator = DraggableGenerator(ctx)

        with PendulumEnvironment(ctx, generator, difficulty=0.5) as env:
            actor = HeuristicsPlayer()

            for _ in range(100):
                state = env.reset()
                obs = env.get_observation(state)

                max_len = 75
                i = 0
                done = False

                while not done and i < max_len:
                    env.render()
                    generator.handle_input()

                    action = actor.get_action(obs)
                    obs, reward, done = env.transition(action)

                    i += 1

                    time.sleep(0.02)
