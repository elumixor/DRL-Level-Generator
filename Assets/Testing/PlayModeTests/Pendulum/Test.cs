using System.Collections;
using System.Threading;
using System.Threading.Tasks;
using Common.ByteConversions;
using NUnit.Framework;
using RemoteComputation;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;

namespace Testing.PlayModeTests.Pendulum
{
    public class Test
    {
        // [SetUp]
        // public void SetUp()
        // {
        // Console.WriteLine("before communicator initialize");
        // RemoteComputation.Communicator.Initialize();
        // }

        [TearDown] public void TearDown() { Communicator.Close(); }

        [UnityTest]
        public IEnumerator AnimationWorks()
        {
            SceneManager.LoadScene("Pendulum");
            yield return null;

            var environment = Object.FindObjectOfType<Environment>();
            var pendulum = Object.FindObjectOfType<Pendulum>();
            var generator = new Generator();

            var generatedData = generator.Generate(0);

            // Setup stuff
            var state = environment.ResetEnvironment(generatedData);
            environment.RenderState(state);

            Debug.Log("Set Up Done");
            yield return null;

            for (var i = 0; i < 10; i++) {
                var (nextState, _, _) = environment.Transition(state, new Action(false));
                environment.RenderState(nextState);
                state = nextState;
                yield return new WaitForSeconds(0.5f);
            }
        }

        [UnityTest]
        public IEnumerator TasksWithCoroutinesWorks()
        {
            var t = Task.Run(() => {
                for (var i = 0; i < 5; i++) {
                    Debug.Log($"Thread {i}");
                    Thread.Sleep(200);
                }

                Debug.Log("Task done");
            });

            for (var i = 0; i < 5; i++) {
                Debug.Log($"Coroutine {i}");
                yield return new WaitForSeconds(0.1f);
            }

            Debug.Log("Waiting for the task to finish...");
            yield return new WaitUntil(() => t.IsCompleted);

            Debug.Log("Coroutine done");
        }

        [UnityTest]
        public IEnumerator PendulumTrainingWorks()
        {
            SceneManager.LoadScene("Pendulum");
            yield return null;

            var environment = Object.FindObjectOfType<Environment>();
            var pendulum = Object.FindObjectOfType<Pendulum>();
            var generator = new Generator();

            var generatedData = generator.Generate(0);

            // Setup stuff
            var state = environment.ResetEnvironment(generatedData);
            environment.RenderState(state);

            Debug.Log("Set Up Done");
            yield return null;

            // Start training

            var dqnTask = MainController.ObtainModel<DQNPendulumActor>(State.SIZE.ToBytes(), Action.SIZE.ToBytes());
            yield return new WaitUntil(() => dqnTask.IsCompleted);

            Assert.IsTrue(dqnTask.IsCompleted);

            var dqnActor = dqnTask.Result;

            Debug.Log(dqnActor);
        }
    }
}
