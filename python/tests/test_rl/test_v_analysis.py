import glfw
import matplotlib.pyplot as plt
import numpy as np
import torch

from core import Trajectory
from core.agents.dqn import DQNAgent
from environments.pendulum import configurations2parameters, PendulumStaticConfiguration, EnemyStaticConfiguration, \
    PendulumDynamicConfiguration, EnemyDynamicConfiguration, PendulumEnvironment
from rendering import RenderingContext

if __name__ == '__main__':
    with RenderingContext(800, 600) as ctx:
        with PendulumEnvironment(ctx) as env:
            pendulum_static_configuration = PendulumStaticConfiguration(0.15, np.deg2rad(30), 0.5, 0.02)
            pendulum_dynamic_configuration = PendulumDynamicConfiguration(np.deg2rad(30), 0, np.deg2rad(5))

            enemies_static_configurations = [EnemyStaticConfiguration(0.1, 0.25, 0.25)]
            enemies_dynamic_configurations = [EnemyDynamicConfiguration()]

            generated_parameters = configurations2parameters(pendulum_static_configuration,
                                                             enemies_static_configurations,
                                                             pendulum_dynamic_configuration,
                                                             enemies_dynamic_configurations)
            env.setup(generated_parameters)

            agent = DQNAgent(env, buffer_capacity=100000)
            file_name = "dqn.pt"
            agent.load(file_name)

            with torch.no_grad():
                t = Trajectory.sample(env, agent, cutoff_at=75)
                v = agent.get_trajectory_values(t).cpu().numpy()

                i = 0

                fig, ax = plt.subplots()


                def update_plot():
                    ax.clear()
                    ax.set_title("V-value")
                    ax.plot(v)
                    fig.show()
                    ax.axvline(x=i)
                    ax.set_xlabel(f"step={i}")
                    ax.set_ylabel(f"V={v[i]:0.4f}")
                    fig.tight_layout()


                env.set_state(t[i][0])
                update_plot()

                while not ctx.is_key_pressed(glfw.KEY_ESCAPE):
                    env.render()
                    fig.canvas.flush_events()
                    ax.relim()
                    ax.autoscale_view()

                    if ctx.is_key_held(glfw.KEY_LEFT):
                        if i == 0:
                            print("Is at starting state")
                            continue

                        i -= 1
                        env.set_state(t[i][0])
                        update_plot()

                    elif ctx.is_key_held(glfw.KEY_RIGHT):
                        if i == len(t):
                            print("Is at last state")
                            continue

                        elif i == (len(t) - 1):
                            env.set_state(t[i][-1])
                            update_plot()
                            i += 1
                        else:
                            env.set_state(t[i][0])
                            update_plot()
                            i += 1
