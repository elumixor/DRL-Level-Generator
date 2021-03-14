from typing import Optional, Tuple

import torch

from core import Environment


class EnvWrapper(Environment):
    def __init__(self, env):
        self.env = env

    def render(self):
        self.env.render()

    @property
    def state_size(self) -> int:
        return self.env.observation_space.shape[0]

    @property
    def action_size(self) -> int:
        return self.env.action_space.n

    def reset(self, difficulty: Optional[float] = None, seed: Optional[float] = None) -> torch.Tensor:
        return torch.from_numpy(self.env.reset()).type(torch.float32)

    def transition(self, action: torch.Tensor) -> Tuple[torch.tensor, float, bool]:
        state, reward, done, _ = self.env.step(action.item())
        return torch.from_numpy(state).type(torch.float32), reward, done

    def get_observation(self, state):
        return state
