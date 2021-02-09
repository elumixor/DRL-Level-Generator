from math import sqrt
from typing import List, Optional, Dict

import matplotlib.pyplot as plt

from common import LRUList


def nice_plot_layout(num_items):
    rows = round(sqrt(num_items))
    columns = num_items // rows
    total = rows * columns
    while total < num_items:
        rows += 1
        total = rows * columns

    return rows, columns


class Logger:
    def __init__(self, print_names, plot_names, capacity=100, plot_columns=3, row_size=5, col_size=3):
        self.capacity = capacity
        self.epoch = 1
        self.max_allowed_columns = plot_columns

        self.print_names = print_names
        self.plot_names = plot_names

        self.names: Optional[List] = None
        self.values: Optional[Dict] = None
        self.plots: Optional[List] = None

        if len(plot_names) != 0:
            num_plots = len(self.plot_names)
            rows, columns = nice_plot_layout(num_plots)
            fig, axs = plt.subplots(nrows=rows, ncols=columns, figsize=(rows * row_size, columns * col_size))
            self.plots = [axs] if len(self.plot_names) == 1 else axs.flatten()

        self.plots = [(plot_names[i], self.plots[i]) for i in range(len(plot_names))]

    def update(self, **kwargs):
        if self.values is None:
            self._initialize(**kwargs)
        else:
            for name, value in kwargs.items():
                self.values[name].append(value)

            self.epoch += 1

    def print(self):
        print(f"Epoch: {self.epoch}")

        for name in self.print_names:
            if name not in self.print_names:
                continue

            value = self.values[name]

            print(f"\t{name}: {value[-1]:10.5f}")

        print()

    def plot(self):
        if len(self.plot_names) == 0:
            return

        epochs = range(max(0, self.epoch - self.capacity), self.epoch)

        for name, ax in self.plots:
            if name not in self.plot_names:
                continue

            value = self.values[name]

            ax.clear()
            ax.set_title(name)
            ax.plot(epochs, [*value])
            ax.grid(color='black', linestyle='-', linewidth=.1)

        plt.draw()
        plt.tight_layout()
        plt.pause(0.001)

    def _initialize(self, **kwargs):
        self.names = [name for name in kwargs]
        self.values = {name: LRUList(kwargs[name], capacity=self.capacity) for name in self.names}

    def __len__(self):
        return 0 if self.values is None else len(self.values)
