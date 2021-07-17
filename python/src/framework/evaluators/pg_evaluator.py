import torch
from torch import Tensor

from .abstract_weighted_evaluator import AbstractWeightedEvaluator
from ..agents import PGAgent


class PGEvaluator(AbstractWeightedEvaluator[PGAgent]):
    def evaluate(self, states: Tensor) -> Tensor:
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
                    trajectory_difficulty = self.evaluate_trajectory(state, agent)
                    difficulties[i_state][i_agent][i_evaluation] = trajectory_difficulty

        # Weight together the evaluations for the same agent
        difficulties = difficulties.mean(dim=-1)

        # Weight together the evaluations by all agents
        difficulties = (difficulties * self.weights).sum(dim=-1, keepdims=True)

        return difficulties

    def evaluate_trajectory(self, state: Tensor, agent: PGAgent):
        """
        Evaluates a trajectory starting at the state by a particular agent, returns difficulty of the trajectory
        :param state: Starting state of the trajectory
        :param agent: Agent to infer actions
        :return: The difficulty of the trajectory, minimum Q-value, maximum Q-value
        """
        states = [state]

        # Sample the trajectory
        for _ in range(self.max_trajectory_length):
            action = agent.get_action(state)
            state, reward, done = self.environment.transition(state, action)

            states.append(state)

            if done:
                break

        # Transform a list into a tensor
        states = torch.tensor(states)

        # Get difficulty of states using the agent
        return agent.get_state_difficulty(states)
