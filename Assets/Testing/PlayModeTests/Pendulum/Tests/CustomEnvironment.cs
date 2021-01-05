using System.Collections;
using Testing.PlayModeTests.Pendulum.Generators;
using Testing.PlayModeTests.Pendulum.StateRenderers;
using UnityEngine;
using UnityEngine.TestTools;

namespace Testing.PlayModeTests.Pendulum.Tests
{
    public class CustomEnvironment : PendulumFixture<PlacedGenerator, PlacedRenderer>
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
            var genData = new CustomGenerator().Generate(0.5f);
            var state = environment.ResetEnvironment(genData);
            stateRenderer.Setup(genData);
            stateRenderer.RenderState(state);
        }
    }
}
