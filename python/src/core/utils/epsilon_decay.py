from serialization import auto_serialized


@auto_serialized
class EpsilonDecay:
    def __init__(self, initial=1, end=0.01, iterations=500):
        self.initial = initial
        self.end = end
        self.iterations = iterations

        self.epsilon = float(self.initial)
        self.elapsed_epochs = 0

    def decay(self):
        r = max((self.iterations - self.elapsed_epochs), 0.0) / self.iterations
        self.epsilon = (self.initial - self.end) * r + self.end
        self.elapsed_epochs += 1

    @property
    def value(self):
        return float(self)

    def __float__(self):
        return self.epsilon

    def __repr__(self):
        return f"Current: {self.epsilon:.2f}. Elapsed: {self.elapsed_epochs}/{self.iterations}"

    def eval(self):
        self.epsilon = 0.0

    def train(self):
        r = max((self.iterations - self.elapsed_epochs), 0.0) / self.iterations
        self.epsilon = (self.initial - self.end) * r + self.end
