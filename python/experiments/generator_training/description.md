# Generator training

Here we experiment with different ways of fitting the generator:

### Direct gradient propagation (where possible)

- The generator outputs the vector of parameters of the level directly (e.g. enemy positions, various lengths and
  angles).
- The level is evaluated by a differentiable difficulty evaluator. The error is then the difference between the input
  and the output difficulty.

Options:

- Diversity: `[True|False]`
- 