from __future__ import annotations

from typing import Optional

from IPython.display import clear_output


class TrainUntil:
    def __init__(self, threshold, num_items, max_iterations=float("inf"), print_frequency: Optional[int] = None,
                 clear=False):
        self.threshold = threshold
        self.num_items = num_items
        self.max_iterations = max_iterations
        self.clear_output = clear

        assert print_frequency is None or print_frequency > 0
        self.print_frequency = print_frequency

        self.num_accepted = 0
        self.iteration = 0
        self.done = self.max_iterations == 0
        self._loss = None

    @property
    def loss(self):
        return self._loss

    @loss.setter
    def loss(self, value):
        self._loss = value

        if self.print_frequency is not None and self.iteration % self.print_frequency == 0:
            if self.clear_output:
                clear_output(wait=True)

            print(f"Iteration: {self.iteration}, loss: {float(self._loss):.7f}")

        if self.iteration >= self.max_iterations:
            self.done = True

        if value < self.threshold:
            self.num_accepted += 1
            if self.num_accepted >= self.num_items:
                self.done = True
        else:
            self.num_accepted = 0

        self.iteration += 1

        if self.done:
            if self.clear_output:
                clear_output(wait=True)

            print(f"Done after {self.iteration} iteration(s). Loss: {float(self._loss):7f}")

    def __enter__(self):
        self.iteration = 0
        self.num_accepted = 0
        self.done = self.max_iterations == 0

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
