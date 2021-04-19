class ConvergenceChecker:
    def __init__(self, steps=100, threshold=0.01, record_all=True):
        self.threshold = threshold
        self.length = steps
        self.values = []

        if record_all:
            def step(value):
                self.values.append(value)

                if len(self.values) >= self.length:
                    return sum(self.values[-self.length:]) / self.length <= self.threshold
        else:
            def step(value):
                self.values.append(value)

                if len(self.values) > self.length:
                    self.values.pop(0)
                    return sum(self.values) / self.length <= self.threshold

                if len(self.values) == self.length:
                    return sum(self.values) / self.length <= self.threshold

        self.step = step
