from typing import List, Tuple

from .episode import Episode
from .utils import discounted_rewards

State = List[float]
Action = List[float]
Reward = float

Transition = Tuple[State, Action, Reward, State]

Trajectory = List[Transition]
