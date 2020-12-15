using RL;

namespace Testing.PlayModeTests.Pendulum
{
    public class PendulumGenerator : IGenerator<GeneratedData>
    {
        public GeneratedData Generate(float difficulty, float randomSeed = 0) =>
                new GeneratedData(1f,
                                  .25f,
                                  30f,
                                  1f,
                                  2,
                                  new GeneratedData.CircleConfiguration(1f, 1f, .25f),
                                  new GeneratedData.CircleConfiguration(-1f, 1f, .25f));
    }
}
