import warnings

import matplotlib.pyplot as plt

from utilities.buffer import Buffer
from utilities.math_utilities import running_average

plt.ion()


def log(message):
    print(f"[P]: {message}")


class Plotter:

    def __init__(self, num_plots=1, plot_width=6, plot_height=3, last_epochs_to_plot_count=100, titles=None, frequency=5):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.fig, self.axs = plt.subplots(num_plots, figsize=(plot_width, plot_height * num_plots))

        if num_plots == 1:
            self.axs = [self.axs]

        self.titles = [] if titles is None else titles
        self.plot_frequency = frequency
        self.epoch = 0

        self.mean_total_rewards = Buffer(last_epochs_to_plot_count)
        self.min_total_rewards = Buffer(last_epochs_to_plot_count)
        self.max_total_rewards = Buffer(last_epochs_to_plot_count)

        self.epoch_mean_total_reward = 0

    def update(self, epoch_training_data, **additional_data):
        self._update(epoch_training_data, **additional_data)

        if self.epoch % self.plot_frequency == 0:
            for i, axs in enumerate(self.axs):
                # Clear already plotted data
                axs.clear()

                axs.set_title(self.titles[i] if i < len(self.titles) else f"Data {i}")

            self._plot_data(epoch_training_data, **additional_data)

        plt.draw()
        plt.tight_layout()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            plt.pause(0.001)

        self.epoch += 1

    def _plot_data(self, epoch_training_data, **additional_data):

        # Plot mean total reward for all episodes in an epoch, and the running average
        mean_total_rewards_count = len(self.mean_total_rewards)
        epochs = [x + max(self.epoch - mean_total_rewards_count, 0) for x in range(mean_total_rewards_count)]

        self.axs[0].plot(epochs, self.mean_total_rewards, label="Mean")
        self.axs[0].plot(epochs, running_average(self.mean_total_rewards), label="Running mean")
        self.axs[0].plot(epochs, self.min_total_rewards, label="Min")
        self.axs[0].plot(epochs, self.max_total_rewards, label="Max")
        self.axs[0].grid(color='black', linestyle='-', linewidth=.1)
        self.axs[0].legend()

        log(f"Epoch: {self.epoch:6}:\t"
            f"{self.epoch_min_total_reward:10.2f} "
            f"{self.epoch_mean_total_reward:10.2f} "
            f"{self.epoch_max_total_reward:10.2f}")

    def _update(self, epoch_training_data, **additional_data):
        # TODO: check if this is the first time we are plotting, and if so, then initialize the plots

        total_rewards = [rewards.sum() for _, _, rewards, _ in epoch_training_data]

        self.epoch_mean_total_reward = sum(total_rewards) / len(total_rewards)
        self.epoch_min_total_reward = min(total_rewards)
        self.epoch_max_total_reward = max(total_rewards)

        self.mean_total_rewards.push(self.epoch_mean_total_reward)
        self.min_total_rewards.push(self.epoch_min_total_reward)
        self.max_total_rewards.push(self.epoch_max_total_reward)
