using System.Collections;
using Common.RandomValues;
using RL;
using Testing.PlayModeTests.Pendulum.Generators;
using Testing.PlayModeTests.Pendulum.StateRenderers;
using Testing.TestCommon;
using UnityEngine.TestTools;

namespace Testing.PlayModeTests.Pendulum.Tests
{
    public class TrainingTests : PendulumFixture<AdaptiveGenerator, StateRenderer>
    {
        // General training should look like this:

        [UnityTest]
        public IEnumerator TrainOnStaticEnvironment()
        {
            yield return Experiment.SetDefaultLogOptions(dqn);
            yield return Experiment.PerformTrainingExperiment(new CustomGenerator(),
                                                              dqn,
                                                              stateRenderer,
                                                              environment,
                                                              dqn,
                                                              1,
                                                              1,
                                                              1,
                                                              5,
                                                              0.5f,
                                                              0.05f);
        }

        class GeneratorYFixed : IGenerator<GeneratedData>
        {
            /// <inheritdoc/>
            public GeneratedData Generate(float difficulty, float randomSeed = 0) =>
                    new GeneratedData(1f,
                                      .25f,
                                      30f,
                                      1f,
                                      10f,
                                      1,
                                      new GeneratedData.CircleConfiguration(UniformValue.Get(-1f, 1f), 1f, .25f));
        }

        [UnityTest]
        public IEnumerator OneEnemyYFixed()
        {
            yield return Experiment.SetDefaultLogOptions(dqn);
            yield return Experiment.PerformTrainingExperiment(new GeneratorYFixed(),
                                                              dqn,
                                                              stateRenderer,
                                                              environment,
                                                              dqn,
                                                              10,
                                                              100,
                                                              10,
                                                              2,
                                                              0.5f,
                                                              0.05f);
        }
    }
}
