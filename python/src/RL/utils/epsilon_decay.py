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

    @property
    def value(self):
        return float(self)

    def __float__(self):
        return self.epsilon
