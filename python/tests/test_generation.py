import glfw

from environments.pendulum import PendulumEnvironment
from environments.pendulum.generator import Generator
from rendering import RenderingContext

if __name__ == '__main__':
    with RenderingContext(800, 600) as rc:
        with PendulumEnvironment(rc) as env:
            generator = Generator()

            generated_parameters = generator()
            env.setup(generated_parameters)
            env.reset()
            env.render()

            while True:
                rc.render_frame()
                if rc.is_key_pressed(glfw.KEY_ESCAPE):
                    break

                elif rc.is_key_pressed(glfw.KEY_SPACE):
                    generated_parameters = generator()
                    env.setup(generated_parameters)
                    env.reset()
                    env.render()
