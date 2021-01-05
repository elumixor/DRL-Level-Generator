using System;
using Common.RandomValues;
using RL;

namespace Testing.PlayModeTests.Pendulum.Generators
{
    [Serializable]
    public class Generator : IGenerator<GeneratedData>
    {
        public readonly IRandomValue<int> enemyCount;
        public readonly IRandomValue enemyRadius;
        public readonly IRandomValue enemyX;
        public readonly IRandomValue enemyY;

        public Generator(IRandomValue<int> enemyCount, IRandomValue enemyRadius, IRandomValue enemyX, IRandomValue enemyY)
        {
            this.enemyCount  = enemyCount;
            this.enemyRadius = enemyRadius;
            this.enemyX      = enemyX;
            this.enemyY      = enemyY;
        }

        public GeneratedData Generate(float difficulty, float randomSeed = 0)
        {
            var ec = enemyCount.Sample;
            var enemies = new GeneratedData.CircleConfiguration[ec];

            for (var i = 0; i < ec; i++)
                enemies[i] = new GeneratedData.CircleConfiguration(enemyX.Sample, enemyY.Sample, enemyRadius.Sample);

            return new GeneratedData(1f, .25f, 30f, 1f, 5f, ec, enemies);
        }
    }
}
