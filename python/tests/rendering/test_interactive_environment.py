from environments.interactive_environment import InteractiveEnvironment
from rendering import RenderingContext

if __name__ == '__main__':
    with RenderingContext(800, 600) as context:
        env = InteractiveEnvironment(context)

        initial_state = env.reset()

        done = False
        while not done:
            action, reward, next_state, done = env.apply_action()
            env.render()
