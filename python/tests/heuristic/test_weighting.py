import wandb

if __name__ == '__main__':
    api = wandb.Api()
    print("Created API")

    runs = [r for r in api.runs("elumixor/Heuristic", filters={"config.Share": True}) if "Enemy X" in r.name]
    print(f"Obtained runs ({len(runs)})")

    enemy_positions = [(run.config["Enemy x"], run.history(keys=["Difficulty", "Randomness"], pandas=False))
                       for run in runs]
    print(f"Selected data")

    difficulties_per_positions = {}


    def get_weight(randomness):
        return 1


    for x, entries in enemy_positions:
        weighted_difficulty = 0
        weights_sum = 0

        for entry in entries:
            difficulty, randomness = entry["Difficulty"], entry["Randomness"]
            weight = get_weight(randomness)
            weights_sum += weight
            weighted_difficulty += weight * difficulty

        weighted_difficulty /= weights_sum

        print(f"Weighted difficulty for enemy x {x}, {weighted_difficulty}")
        difficulties_per_positions[x] = weighted_difficulty

    run = wandb.init(project="Heuristic", name="Uniform", tags=["Difficulty comparison", "Weighting"])

    for key, value in difficulties_per_positions.items():
        wandb.log({"x": key, "Difficulty (aggregated)": value})

    run.finish()
