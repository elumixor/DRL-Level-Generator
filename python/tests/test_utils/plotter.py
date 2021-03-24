import math

from matplotlib import pyplot as plt

from utilities.recorder import Recorder


class Plotter(Recorder):
    def log(self, **kwargs):
        self.record(**kwargs)

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
