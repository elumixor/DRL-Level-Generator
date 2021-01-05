using RL;

namespace Testing.PlayModeTests.Pendulum.Generators
{
    public class CustomGenerator : IGenerator<GeneratedData>
    {
        /// <inheritdoc/>
        public GeneratedData Generate
                (float difficulty, float randomSeed = 0) =>
                new GeneratedData(1f, .25f, 30f, 1f, 5f, 1, new GeneratedData.CircleConfiguration(1f, 1f, .25f));
    }
}
