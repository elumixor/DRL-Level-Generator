import numpy as np
import matplotlib.pyplot as plt

X = np.array([-3, 1, 0, 0, 2, -1])
space = np.linspace(-4, 3, 100)


def k(x):
    if np.abs(x) <= 3 / 2:
        return 1 / 3
    return 0


def value(x):
    return np.mean([k(x_) for x_ in (x - X)])


y = [value(x_) for x_ in space]
plt.plot(space, y)
plt.show()

print(value(0))