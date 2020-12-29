using System.Collections;
using UnityEngine;
using UnityEngine.TestTools;

namespace Testing.PlayModeTests.Pendulum.Tests
{
    public class Generation : PendulumFixture
    {
        bool done;
        State state;

        [UnityTest]
        public IEnumerator VisualGenerationCheck()
        {
            while (true) {
                if (Input.GetKeyDown(KeyCode.Alpha0)) {
                    GenerateNext(0);
                    yield return null;
                } else if (Input.GetKeyDown(KeyCode.Alpha1)) {
                    GenerateNext(1);
                    yield return null;
                } else if (Input.GetKeyDown(KeyCode.Alpha2)) {
                    GenerateNext(2);
                    yield return null;
                } else if (Input.GetKeyDown(KeyCode.Alpha3)) {
                    GenerateNext(3);
                    yield return null;
                } else if (Input.GetKeyDown(KeyCode.Space)) {
                    Step();
                    yield return null;
                } else if (Input.GetKeyDown(KeyCode.Escape)) {
                    Debug.Log("Escape...");
                    yield break;
                }

                yield return null;
            }
        }

        void GenerateNext(int level)
        {
            Debug.Log("Generating difficulty " + level);
            done = false;
            var generatedData = generator.Generate(level);
            state = environment.ResetEnvironment(generatedData);
            stateRenderer.Setup(generatedData);
            Step();
        }

        void Step()
        {
            if (state == null) {
                Debug.Log("State is null");
                return;
            }

            if (this.done) {
                Debug.Log("Trajectory is finished (done)");
                return;
            }

            stateRenderer.RenderState(state);

            var action = dqn.GetAction(state.Observation);
            var (nextState, _, done) = environment.Transition(state, action);

            this.done = done;
            state     = nextState;
        }
    }
}
