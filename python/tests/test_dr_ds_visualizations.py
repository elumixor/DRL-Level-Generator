import matplotlib.pyplot as plt
import numpy as np

import wandb

plt.ioff()

if __name__ == '__main__':
    run = wandb.init(project="Heuristic", tags=["Derivative", "Relaxed"], name="Increase truthness")

    x = np.linspace(-2, 2, 101)
    y = np.where(x <= 0, 1, 0).tolist()
    x = x.tolist()

    x.insert(51, 0)
    y.insert(51, 0)

    for x, y in zip(x, y):
        wandb.log({"distance": x, "derivative": y})

    run.finish()

    run = wandb.init(project="Heuristic", tags=["Derivative", "Relaxed"], name="Increase falseness")

    x = np.linspace(-2, 2, 101)
    y = np.where(x <= 0, 0, 1).tolist()
    x = x.tolist()

    x.insert(51, 0)
    y.insert(51, 1)

    for x, y in zip(x, y):
        wandb.log({"distance": x, "derivative": y})

    run.finish()

    run = wandb.init(project="Heuristic", tags=["Derivative", "Relaxed"], name="Increase truthness")

    x = np.linspace(-2, 2, 101)
    y = np.where(x <= 0, 1, -1).tolist()
    x = x.tolist()

    x.insert(51, 0)
    y.insert(51, 0)

    for x, y in zip(x, y):
        wandb.log({"distance": x, "derivative": y})

    run.finish()

    run = wandb.init(project="Heuristic", tags=["Derivative", "Relaxed"], name="Increase falseness")

    x = np.linspace(-2, 2, 101)
    y = np.where(x <= 0, -1, 1).tolist()
    x = x.tolist()

    x.insert(51, 0)
    y.insert(51, 1)

    for x, y in zip(x, y):
        wandb.log({"distance": x, "derivative": y})

    run.finish()
