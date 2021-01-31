from typing import Tuple, Any

import numpy as np

from ..renderable_environment import RenderableEnvironment
from rendering import RenderingContext


class PendulumEnvironment(RenderableEnvironment):
    def __init__(self, rendering_context: RenderingContext):
        super().__init__(rendering_context)

        # We need several objects

        # Line
        # Actual pendulum
        # Enemies

    @property
    def observation_space(self):
        pass

    @property
    def action_space(self):
        pass

    def reset(self) -> np.ndarray:
        pass

    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, Any]:
        pass

    # Setup
    def setup(self):
        ...
