from typing import List

import numpy as np
from matplotlib import pyplot as plt

from remote_computation.logging import LogOptions, LogData, LogOption, LogOptionName, LogEntry, RangedEntry
from utilities import running_average

plt.ion()


class Logger:

    def __init__(self, model_id: int, options: LogOptions):
        self.model_id = model_id
        self.options = options

        num_plots = options.length

        self.axs = dict()

        _, axs = plt.subplots(num_plots)
        if num_plots == 1:
            axs = [axs]

        i = 0
        self.axs = dict()
        for option_name, _ in options.items():
            self.axs[option_name] = axs[i]
            i += 1

        self.epoch = 0

    def update(self, data: LogData):
        if self.epoch == 0:
            self.epoch += 1
            return

        s = f"[Model {self.model_id}] Epoch {self.epoch}\n"
        do_print = False
        to_plot = []

        for name, option in self.options.items():
            option: LogOption

            if name not in data or self.epoch % option.frequency != 0:
                continue

            entries = data[name]

            if option.print:
                do_print = True
                last = entries[-1]
                s += f"  {name}: {str(last)}\n"

            if option.plot:
                to_plot.append((name, option, entries))

        if do_print:
            print(s)

        if len(to_plot) > 0:
            for name, option, entries in to_plot:
                self.plot(name, option, entries)

            plt.draw()
            plt.tight_layout()

            plt.pause(0.001)

        self.epoch += 1

    def plot(self, name: LogOptionName, option: LogOption, entries: List[LogEntry]):
        ax = self.axs[name]
        example = entries[0]

        # Clear already plotted data
        ax.clear()

        ax.set_title(str(name))

        last_n = min(option.log_last_n, len(entries))
        last = entries[-last_n:]
        data = np.array([item.value for item in last])
        epochs = [x + max(self.epoch - last_n, 0) for x in range(last_n)]

        ax.plot(epochs, data)

        if option.running_average_smoothing != 0.0:
            ax.plot(epochs, running_average(data))

        if isinstance(example, RangedEntry) and option.min_max:
            mins = np.array([item.min_value for item in last])
            maxs = np.array([item.max_value for item in last])

            ax.fill_between(epochs, maxs, mins, alpha=0.2)

        ax.grid(color='black', linestyle='-', linewidth=.1)

    def show(self, data: LogData):
        """Force showing, disregarding frequency, don't increase the current epoch"""

        s = f"[Model {self.model_id}] Epoch {self.epoch}\n"
        do_print = False
        to_plot = []

        for name, option in self.options.items():
            option: LogOption

            if name not in data:
                continue

            entries = data[name]

            if option.print:
                do_print = True
                last = entries[-1]
                s += f"  {name}: {str(last)}\n"

            if option.plot:
                to_plot.append((name, option, entries))

        if do_print:
            print(s)

        if len(to_plot) > 0:
            for name, option, entries in to_plot:
                self.plot(name, option, entries)

            plt.draw()
            plt.tight_layout()

            plt.pause(0.001)
