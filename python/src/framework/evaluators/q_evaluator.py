from typing import List

import torch
from torch import Tensor

from .abstract_weighted_evaluator import AbstractWeightedEvaluator
from ..agents import AbstractQAgent
from ..environments import AbstractEnvironment


class QEvaluator(AbstractWeightedEvaluator[AbstractQAgent]):
    def __init__(self, environment: AbstractEnvironment, agents: List[AbstractQAgent], weights: List[float],
                 num_evaluations: int = 1, max_trajectory_length: int = 1):
        super().__init__(environment, agents, weights, num_evaluations, max_trajectory_length)

        # The biggest, and smallest Q-values
        # Used for normalization to obtain difficulties in the [0, 1] range
        self.q_max = float("-inf")
        self.q_min = float("inf")

    def evaluate(self, states: Tensor) -> Tensor:
        # Handle single state input
        do_unsqueeze = states.ndim == 1
        if do_unsqueeze:
            states = states.reshape([1, -1])

        # First, let's collect trajectory rewards
        difficulties = torch.zeros((states.shape[0], len(self.agents), self.num_evaluations))

        # todo: this can (and should) be done in parallel

        # Find the difficulty of each state
        for i_state, state in enumerate(states):

            # Evaluate state by each agent
            for i_agent, (agent, weight) in enumerate(zip(self.agents, self.weights)):

                # For each agent, run several trials on the trajectory for the cases where
                # an agent uses stochastic strategy, or environment is stochastic
                for i_evaluation in range(self.num_evaluations):
                    # Evaluate the trajectory
                    trajectory_difficulty, q_min, q_max = self.sample_trajectory(state, agent)
                    difficulties[i_state][i_agent][i_evaluation] = trajectory_difficulty

                    # Update bounds for normalization
                    self.q_max = max(self.q_max, q_max)
                    self.q_min = min(self.q_min, q_min)

        # Normalize the difficulties using the maximum and minimum Q-values
        difficulties = self.normalize(difficulties)

        # Weight together the evaluations for the same agent
        difficulties = difficulties.mean(dim=-1)

        # Weight together the evaluations by all agents
        difficulties = (difficulties * self.weights).sum(dim=-1, keepdims=True)

        return difficulties.squeeze()

    def sample_trajectory(self, state: Tensor, agent: AbstractQAgent):
        """
        Evaluates a trajectory starting at the state by a particular agent, returns q-values of that trajectory
        :param state: Starting state of the trajectory
        :param agent: Agent to infer actions
        :return: The difficulty of the trajectory, minimum Q-value, maximum Q-value
        """
        trajectory_difficulty = 0.0
        q_max = float("-inf")
        q_min = float("inf")

        for trajectory_length in range(self.max_trajectory_length):
            # Get Q-values using the agent
            q_values = agent.get_q_values(state)

            # Calculate state difficulty
            q_values_max = q_values.max()
            state_difficulty = q_values_max - q_values.mean()

            # Update trajectory difficulty
            trajectory_difficulty += state_difficulty

            # Update bounds
            q_max = max(q_max, q_values_max)
            q_min = min(q_min, q_values.min())

            action = agent.get_action(state)
            state, reward, done = self.environment.transition(state, action)

            if done:
                break

        # Average the individual states' difficulties
        trajectory_difficulty /= (trajectory_length + 1)

        return trajectory_difficulty, q_min, q_max

    def normalize(self, difficulties):
        return difficulties / (self.q_max - self.q_min)
