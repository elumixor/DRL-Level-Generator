# Level Generator

[GitHub](https://github.com/elumixor/DRL-Level-Generator/tree/global/python_opengl/python)

### Structure

1. `experiments` contains notebooks with use-cases for the framework:
   1. `1_differnetiable_evaluator` shows the general framework idea of using NN generator, NN evaluator, and an Oracle.
      A heuristic pendulum oracle is used there.

   2. `2_diversity` shows the N-seeded generator approach to generate multiple levels

   3. `3_decreasing_offsets_weight` shows the impact of gradually decreasing the weight of the offsets loss

   4. `4_q_learning` shows the DQN agent learning to operate within the pendulum environment

   5. `5_evaluators` compares various oracles (introducing the Q-values oracle). In the end, we train the NN evaluator
      on the trajectory rewards oracle

   6. `6_multiple_enemies` increases the number of enemies to 2 and 3. However, it's tricky to visualize the results

2. `src` contains the main code for the framework and its components:

   1. `framework` contains the main code with generators, evaluators. It's the domain-free framework.

   2. `pendulum` contains the pendulum environment, and components specific to it - heuristic oracle, agent, etc.

   3. `rendering` is a layer of abstraction over the OpenGL to simplify rendering.

   4. `utils` contains various utility functions

