using System.Collections;
using RL;
using UnityEngine;
using UnityEngine.Assertions;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;

namespace Testing.PlayModeTests.DummyEnvironment
{
    public class RendererTest
    {
        class MyState : Vector
        {
            public MyState(float x) : base(x) { }
        }

        class MyEnvironment : IEnvironment, IStateRenderer
        {
            readonly Transform actor;

            public MyEnvironment(Transform actor) => this.actor = actor;

            public Vector ResetEnvironment(Vector generatedData) =>
                    // should return initial state
                    new MyState(3f);

            public (Vector nextState, float reward, bool done) Transition(Vector state, Vector action)
            {
                // apply horizontal movement
                // end when >= 5
                // reward = 1 if in game, 0 if terminal
                var nextPosition = state[0] + action[0];
                var nextState = new MyState(nextPosition);
                var done = nextPosition >= 5f;
                var reward = done ? 0f : 1f;

                return (nextState, reward, done);
            }

            /// <inheritdoc/>
            public void Setup(Vector generatedData) { }

            public void RenderState(Vector state) { actor.position = Vector3.right * state[0]; }
        }

        class MyActor : IActor
        {
            public Vector GetAction(Vector obs) => new Vector(1);
        }

        [UnityTest]
        public IEnumerator EnvironmentSetupShouldWork()
        {
            SceneManager.LoadScene("Testing/PlayModeTests/DummyEnvironment/StateRendererTestScene");

            yield return new WaitForSeconds(1);

            var actor = new GameObject("Actor");
            Debug.Log(actor);

            Assert.AreEqual(actor.transform.position, Vector3.zero);
            Assert.IsNotNull(actor);

            // get some game objects, initialize custom state renderer with references, etc.
            var environment = new MyEnvironment(actor.transform);

            var state = environment.ResetEnvironment(new Vector());
            environment.RenderState(state);
            Assert.AreEqual(actor.transform.position, Vector3.right * 3f);

            var myActor = new MyActor();
            var action = myActor.GetAction(state);
            Assert.AreEqual(action, new Vector(1f));
            var (nextState, reward, done) = environment.Transition(state, action);
            Assert.AreEqual(nextState, new MyState(3f + 1f));
            Assert.AreEqual(reward, 1f);
            Assert.IsFalse(done);

            environment.RenderState(nextState);
            Assert.AreEqual(actor.transform.position, Vector3.right * (3f + 1f));

            state  = nextState;
            action = myActor.GetAction(state);

            var (terminalState, reward1, done1) = environment.Transition(state, action);
            Assert.AreEqual(terminalState, new MyState(3f + 2f));
            Assert.AreEqual(reward1, 0f);
            Assert.IsTrue(done1);

            environment.RenderState(terminalState);
            Assert.AreEqual(actor.transform.position, Vector3.right * (3f + 2f));

            yield return new WaitForSeconds(1);
        }
    }
}
