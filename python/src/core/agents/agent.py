from abc import abstractmethod, ABC


class Agent(ABC):
    @abstractmethod
    def get_action(self, observation):
        ...

    @abstractmethod
    def update(self, trajectories):
        ...

    def eval(self):
        ...

    def print_data(self):
        pass

    def train(self):
        pass
