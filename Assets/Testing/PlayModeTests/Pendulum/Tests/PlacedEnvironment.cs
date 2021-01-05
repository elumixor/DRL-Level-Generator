using System.Collections;
using Testing.PlayModeTests.Pendulum.Generators;
using Testing.PlayModeTests.Pendulum.StateRenderers;
using Testing.TestCommon;
using UnityEngine;
using UnityEngine.TestTools;

namespace Testing.PlayModeTests.Pendulum.Tests
{
    public class PlacedEnvironment : PendulumFixture<PlacedGenerator, PlacedRenderer>
    {
        [UnityTest]
        public IEnumerator Render()
        {
            while (true) {
                if (Input.GetKeyDown(KeyCode.Escape)) yield break;

                if (Input.GetKeyDown(KeyCode.Space)) GenerateAndRender();

                yield return null;
            }
        }

        void GenerateAndRender()
        {
            generator.FindEnemies();
            var genData = generator.Generate(0.5f);
            var state = environment.ResetEnvironment(genData);
            stateRenderer.Setup(genData);
            stateRenderer.RenderState(state);
        }

        [UnityTest]
        public IEnumerator Train()
        {
            var logOptions = Experiment.DefaultLogOptions;

            foreach (var kvp in logOptions.Values) kvp.frequency = 20;

            yield return Experiment.SetLogOptions(dqn, logOptions);

            generator.FindEnemies();

            while (true) {
                if (Input.GetKeyDown(KeyCode.Escape)) yield break;

                if (Input.GetKeyDown(KeyCode.R))
                    yield return Experiment.Render(generator, dqn, stateRenderer, environment, 0.5f, deltaTime: 0.1f);

                if (Input.GetKeyDown(KeyCode.T)) {
                    yield return Experiment.Train(generator, dqn, environment, dqn, 0.5f, 10);
                    yield return Experiment.ShowLog(dqn);
                }

                if (Input.GetKeyDown(KeyCode.S))
                    for (var i = 0; i < 20; i++)
                        yield return Experiment.Train(generator, dqn, environment, dqn, 0.5f, 10);

                yield return null;
            }
        }
    }
}
