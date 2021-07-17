from typing import List

import torch
from torch import Tensor

from .abstract_weighted_evaluator import AbstractWeightedEvaluator
from ..agents import AbstractAgent
from ..environments import AbstractEnvironment


class TrajectoryRewardsEvaluator(AbstractWeightedEvaluator[AbstractAgent]):
    def __init__(self, environment: AbstractEnvironment, agents: List[AbstractAgent], weights: List[float],
                 num_evaluations: int = 1, max_trajectory_length: int = 100):
        """
        :param agents: Agents who can evaluate an level in environment
        :param weights:
        """
        super().__init__(environment, agents, weights, num_evaluations, max_trajectory_length)

        # The biggest, and smallest trajectory rewards.
        # Used for normalization to obtain difficulties in the [0, 1] range
        self.reward_max = float("-inf")
        self.reward_min = float("-inf")

    def evaluate(self, states: Tensor) -> Tensor:
        """
        1. In a specified environment, embeddings are translated into levels.
        2. Then trajectories are sampled using different agents with different skill levels.
        3. The individual difficulties are then weighted and summed using the skill weighting.
        :param states: Level embeddings to evaluate
        :return: Difficulties, shape (num_embeddings, 1)
        """
        # First, let's collect trajectory rewards
        trajectory_rewards = torch.zeros((states.shape[0], len(self.agents), self.num_evaluations))

        # todo: this can (and should) be done in parallel

        # Find the difficulty of each state
        for i_state, state in enumerate(states):

            # Evaluate state by each agent
            for i_agent, (agent, weight) in enumerate(zip(self.agents, self.weights)):

                # For each agent, run several trials on the trajectory for the cases where
                # an agent uses stochastic strategy, or environment is stochastic
                for i_evaluation in range(self.num_evaluations):
                    # Evaluate the trajectory
                    trajectory_reward = self.evaluate_trajectory(state, agent)
                    trajectory_rewards[i_state][i_agent][i_evaluation] = trajectory_reward

        # Update the biggest and the smallest trajectory rewards
        self.reward_max = max(self.reward_max, trajectory_rewards.max())
        self.reward_min = max(self.reward_min, trajectory_rewards.min())

        # Calculate the difficulties
        difficulties = (self.reward_max - trajectory_rewards) / (self.reward_max - self.reward_min)

        # Weight together the evaluations for the same agent
        difficulties = difficulties.mean(dim=-1)

        # Weight together the evaluations by all agents
        difficulties = (difficulties * self.weights).sum(dim=-1, keepdims=True)

        return difficulties

    def evaluate_trajectory(self, state: Tensor, agent: AbstractAgent):
        """
        Evaluates a trajectory starting at the state by a particular agent
        :param state: Starting state of the trajectory
        :param agent: Agent to infer actions
        :return: Total (not discounted) reward of the trajectory
        """
        total_reward = 0.0

        for _ in range(self.max_trajectory_length):
            action = agent.get_action(state)
            state, reward, done = self.environment.transition(state, action)
            total_reward += reward

            if done:
                break

        return total_reward
