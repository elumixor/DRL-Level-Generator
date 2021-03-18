from evaluators import DirectEvaluator
from experiments import run_current


def main(context, max_angle, enemy_x_min, enemy_x_max, connector_length, enemy_radius, bob_radius, epochs, batch_size,
         lr, constrain, input_difficulty_sampling, diversity, diversity_weight, constrain_weight):
    evaluator = DirectEvaluator(connector_length, max_angle, enemy_radius, bob_radius)


if __name__ == '__main__':
    run_current()
