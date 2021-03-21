import math

from matplotlib import pyplot as plt


class Plotter:
    def __init__(self):
        self.entries = dict()

    def log(self, **kwargs):
        for name, value in kwargs.items():
            if name not in self.entries:
                arr = []
                self.entries[name] = arr
            else:
                arr = self.entries[name]

            arr.append(value)

    def show(self):
        num_plots = len(self.entries)
        rows = math.floor(math.sqrt(num_plots))
        columns = math.ceil(num_plots / rows)

        fig, axs = plt.subplots(rows, columns)

        for i, (name, value) in enumerate(self.entries.items()):
            c = i // rows
            r = i % rows

            axs[r][c].plot(value)
            axs[r][c].set_title(name)

        plt.show()
