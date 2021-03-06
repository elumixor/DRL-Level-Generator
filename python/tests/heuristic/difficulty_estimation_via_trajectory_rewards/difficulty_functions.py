import numpy as np
import wandb

if __name__ == '__main__':
    subdivisions = 1001
    t = np.linspace(0, 10, subdivisions)
    weight = 10 / subdivisions

    a = 1 / (t + 1) ** 2, "1 / (t + 1)^2"
    b = np.sin(t) / ((t + 1) ** 2), "sin(t) / (t + 1)^2"
    c = np.sin(t) / (2 * t), "sin(t) / 2t"
    d = np.sin(t) / 2, "sin(t) / 2"

    c[0][np.isnan(c[0])] = 0.5

    for y, name in [a, b, c, d]:
        run = wandb.init(project="Heuristic", name=f"Skill growth function",
                         tags=["Difficulty comparison", "Growth"],
                         config={"name": name})

        for t1, y1 in zip(t, y):
            wandb.log({"t": t1, "y": y1})

        run.finish()

        y = np.cumsum(y * weight)
        run = wandb.init(project="Heuristic", name=f"Skill function",
                         tags=["Difficulty comparison", "Skill"],
                         config={"name": name})

        for t1, y1 in zip(t, y):
            wandb.log({"t": t1, "y": y1})

        run.finish()
