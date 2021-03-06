import wandb
from scipy.stats import skewnorm

from common import log

if __name__ == '__main__':
    api = wandb.Api()
    print("Created API")

    runs = [r for r in api.runs("elumixor/Heuristic", filters={"config.Share": True}) if "Enemy X" in r.name]
    print(f"Obtained runs ({len(runs)})")

    enemy_positions = [(run.config["Enemy x"], run.history(keys=["Difficulty", "Randomness"], pandas=False))
                       for run in runs]
    print(f"Selected data")

    difficulties_per_positions = {}

    # region Uniform
    for x, entries in enemy_positions:
        weighted_difficulty = 0
        weights_sum = 0

        for entry in entries:
            difficulty, randomness = entry["Difficulty"], entry["Randomness"]
            weight = 1
            weights_sum += weight
            weighted_difficulty += weight * difficulty

        weighted_difficulty /= weights_sum

        print(f"Weighted difficulty for enemy x {x}, {weighted_difficulty}")
        difficulties_per_positions[x] = weighted_difficulty

    run = wandb.init(project="Heuristic", name="Uniform", tags=["Difficulty comparison", "Weighting"])

    for key, value in difficulties_per_positions.items():
        wandb.log({"x": key, "Difficulty": value})

    run.finish()
    # endregion

    # region Skew Normal
    for i, alpha, mu, sigma in zip(range(5), [-2, -1, 0, 1, 2], [-0.25, 0, 0.25, 0.5, 0.75], [1, 1, 0.5, 0.5, 0.25]):
        log.good(f"alpha={alpha}, mu={mu}, sigma={sigma}")

        for x, entries in enemy_positions:
            weighted_difficulty = 0
            weights_sum = 0

            for entry in entries:
                difficulty, randomness = entry["Difficulty"], entry["Randomness"]
                weight = skewnorm.pdf(randomness, alpha, loc=mu, scale=sigma)
                weights_sum += weight
                weighted_difficulty += weight * difficulty

            weighted_difficulty /= weights_sum

            print(f"Weighted difficulty for enemy x {x}, {weighted_difficulty}")
            difficulties_per_positions[x] = weighted_difficulty

        run = wandb.init(project="Heuristic", name=f"Skew-{i}", tags=["Difficulty comparison", "Weighting", "Skew"],
                         config={
                             "alpha": alpha,
                             "mu": mu,
                             "sigma": sigma,
                         })

        for key, value in difficulties_per_positions.items():
            wandb.log({"x": key, "Difficulty": value})

        run.finish()
    # endregion
