from abc import abstractmethod, ABC

import numpy as np

from common import setter
from ..actor import Actor
from ..environments import Environment
from ..trajectory import Trajectory


class Agent(Actor, ABC):
    def __init__(self, env: Environment):
        """
        Agent can operate only in a given environment
        """
        self.env = env

    @abstractmethod
    def train(self, *args, **kwargs):
        """
        A highly-configurable method to train the agent to presumably gain a better performance
        """

    @setter
    def eval(self, value: bool):
        """
        Switches eval or train mode based on the given parameter
        :param value: If true, should set to evaluation mode. If false, should set to training mode
        """

    def save(self, path: str):
        """
        Save the agent to a file. The agent stored should be later used for both training and inference
        """

    def load(self, path: str):
        """
        Load the agent from a file. The agent loaded can be used for both training and inference
        """

    def sample_trajectory(self, maximum_length=np.inf) -> Trajectory:
        """
        Samples a single trajectory with the current parameters.
        Setting the agent to evaluation or training mode is left to the caller.

        :param maximum_length: The maximum length of the trajectory
        :returns: Trajectory, which is a list of tuples (observation, action, reward, done, next observation)
        """

        state = self.env.reset()
        observation = self.env.get_observation(state)

        trajectory = Trajectory()

        i = 0
        done = False
        while not done and i < maximum_length:
            action = self.get_action(observation)
            next_observation, reward, done = self.env.transition(action)

            trajectory.append((observation, action, reward, done, next_observation))
            observation = next_observation
            i += 1

        return trajectory
