using Common.RandomValues;
using RL;
using Testing.PlayModeTests.Pendulum;

namespace Testing.PlayModeTests
{
    public class AdaptiveGenerator : IGenerator<GeneratedData>
    {
        /// <inheritdoc/>
        public GeneratedData Generate(float difficulty, float randomSeed = 0)
        {
            var level = difficulty == 0f ? 0 : difficulty < 0.25f ? 1 : difficulty < 1f ? 2 : 3;

            return Generate(level);
        }

        public GeneratedData Generate(int level)
        {
            const float connectorLength = 1f;
            const float bobRadius = .25f;

            // Randomize starting angle
            var angle = UniformValue.Get(-30f, 30f);

            // Randomize starting angular direction
            var angularDirection = EitherValue.Get(1, -1);

            // Randomize enemies' positions
            var enemies = new GeneratedData.CircleConfiguration[level];

            var radius = level == 1 ? 0.25f : level == 2 ? 0.3f : 1f;

            const float minX = -1f;
            const float maxX = 1f;
            const float minY = 1f;
            const float maxY = 2f;

            var x = new UniformValue(minX, maxX);
            var y = new UniformValue(minY, maxY);

            for (var i = 0; i < level; i++) enemies[i] = new GeneratedData.CircleConfiguration(x.Sample, y.Sample, radius);

            return new GeneratedData(connectorLength, bobRadius, angle, angularDirection, 5f, level, enemies);
        }
    }
}
