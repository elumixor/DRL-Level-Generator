from abc import ABC
from typing import Generic, List, TypeVar

import torch

from framework.environments import AbstractEnvironment
from framework.evaluators import AbstractEvaluator
from utils import approx

TAgent = TypeVar("TAgent")


class AbstractWeightedEvaluator(AbstractEvaluator, Generic[TAgent], ABC):
    def __init__(self, environment: AbstractEnvironment, agents: List[TAgent], weights: List[float],
                 num_evaluations: int = 1, max_trajectory_length: int = 1):
        if len(agents) != len(weights):
            raise Exception(f"Number of agents should be the same as number of weights")

        weights = torch.tensor(weights)

        if not approx(weights.sum(), 1.0):
            raise Exception(f"Weights should sum up to one, but was {sum(weights)}")

        self.environment = environment
        self.agents = agents
        self.weights = weights
        self.num_evaluations = num_evaluations
        self.max_trajectory_length = max_trajectory_length
