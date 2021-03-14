class StepCounter:
    def __init__(self, total: int, frequency: int = 1, name="Step"):
        self.total = total
        self.current = 0
        self.frequency = frequency
        self.name = name

    def step(self):
        self.current += 1

        if (self.current - 1) % self.frequency == 0:
            print(self)

    def __str__(self):
        return f"{self.name} {self.current} out of {self.total} ({self.current / self.total * 100:5.2f}%)"
