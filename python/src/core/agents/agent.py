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

    def print_progress(self):
        pass

    def plot_progress(self):
        pass

    def train(self):
        pass

    def log_progress(self):
        pass

    def save(self, path: str):
        pass

    def load(self, path: str):
        pass
