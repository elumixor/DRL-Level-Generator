import glfw

from environments.pendulum import PendulumEnvironment
from environments.pendulum.generators import NNGenerator
from environments.pendulum.heuristics import HeuristicsPlayer
from rendering import RenderingContext

if __name__ == '__main__':
    with RenderingContext(800, 600) as ctx:
        generator = NNGenerator()
        with PendulumEnvironment(ctx, generator) as env:
            actor = HeuristicsPlayer()
            state = env.reset(0.5)
            obs = env.get_observation(state)

            step = 0
            total_reward = 0
            while not ctx.is_key_held(glfw.KEY_ESCAPE) and step <= 75:
                # env.render()
                # time.sleep(0.0167)

                action = actor.get_action(obs)
                obs, reward, done = env.transition(action)

                total_reward += reward
                step += 1

            total_reward.backward()
            print(state.grad)

            input("Press any key to exit...\n")
