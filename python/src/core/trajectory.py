from __future__ import annotations

import time

from .environments import RenderableEnvironment


class Trajectory(list):
    @property
    def total_reward(self):
        return sum([reward for _, _, reward, _, _, in self])

    def render(self, env: RenderableEnvironment, delta_time=1 / 60):
        for state, *_ in self:
            env.state = state
            env.render()
            time.sleep(delta_time)
