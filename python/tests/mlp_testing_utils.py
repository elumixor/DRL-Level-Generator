import matplotlib.pyplot as plt


def calculate_intermediates(nn, sizes, x):
    intermediates = []
    x1 = x
    for i in range(len(sizes)):
        x1 = nn.activation(nn.layers[i](x1))
        intermediates.append(x1)
    last = nn.layers[len(sizes)](x1)
    return intermediates, last


def plot_intermediates(axs, intermediates, last, x, y, clear=False):
    axs[0][0].plot(x, x.detach().flatten())
    for i, intermediate in enumerate(intermediates):
        num_plots = intermediate.shape[-1]

        for j in range(num_plots):
            axs[j][i + 1].plot(x, intermediate[:, j].detach().flatten())

    axs[0][-1].plot(x, last.detach().flatten())
    axs[0][-1].plot(x, y)

    if not clear:
        return

    plt.draw()
    plt.pause(0.001)
    for ax in axs:
        for a in ax:
            a.clear()
