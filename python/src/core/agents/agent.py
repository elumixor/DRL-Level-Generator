from abc import abstractmethod, ABC


class Agent(ABC):
    @abstractmethod
    def get_action(self, observation):
        ...

    @abstractmethod
    def train(self, trajectories):
        ...

    @abstractmethod
    def eval(self):
        ...
