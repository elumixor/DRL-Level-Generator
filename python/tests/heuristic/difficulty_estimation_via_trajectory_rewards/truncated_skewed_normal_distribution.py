import numpy as np
import wandb
from scipy.stats import skewnorm

if __name__ == '__main__':
    subdivisions = 1001
    x = np.linspace(0, 1, subdivisions)


    def truncated_skew(x, alpha, a, b, loc=0.0, scale=1.0):
        pdf = skewnorm.pdf(x, alpha, loc=loc, scale=scale)
        cdf_a = skewnorm.cdf(a, alpha, loc=loc, scale=scale)
        cdf_b = skewnorm.cdf(b, alpha, loc=loc, scale=scale)
        res = pdf / (cdf_b - cdf_a)
        res[x < a] = 0
        res[x > b] = 0
        return res


    mu = 0.5
    sigma = 0.5
    a = 0
    b = 1

    for alpha, mu, sigma in zip([-2, -1, 0, 1, 2], [-0.25, 0, 0.25, 0.5, 0.75], [1, 1, 0.5, 0.5, 0.25]):
        y = truncated_skew(x, alpha, a, b, loc=mu, scale=sigma)

        run = wandb.init(project="Heuristic", name=f"Distribution",
                         tags=["Difficulty comparison", "Distributions"],
                         config={
                             "alpha": alpha,
                             "mu": mu,
                             "sigma": sigma
                         })

        for x1, y1 in zip(x, y):
            wandb.log({"x": x1, "y": y1})

        run.finish()
