import numpy as np

from .plotter import Plotter


class LeftRightPlotter(Plotter):

    def __init__(self, num_plots=2, plot_width=6, plot_height=3, last_epochs_to_plot_count=100, titles=None, frequency=1):
        super().__init__(num_plots=2, plot_width=6, plot_height=3, last_epochs_to_plot_count=100, titles=None, frequency=1)

    def update(self, epoch_training_data, **additional_data):
        super(LeftRightPlotter, self).update(epoch_training_data, **additional_data)

    def _plot_data(self, epoch_training_data, **additional_data):
        super()._plot_data(epoch_training_data, **additional_data)

        x, p_left_x = additional_data["p_left_x"]

        # Probability of going left
        x_opt = x[np.argmin(np.abs(p_left_x - .5))]
        self.axs[1].plot([-5, 5], [.5, .5], color="red", linewidth=.3)
        self.axs[1].plot([x_opt, x_opt], [0, 1], color="red", linewidth=.3)
        self.axs[1].plot(x, p_left_x)
        self.axs[1].set_ylim([0, 1])
        self.axs[1].grid(color='black', linestyle='-', linewidth=.1)
