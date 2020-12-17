using System.Collections;
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

        // A UnityTest behaves like a coroutine in PlayMode
        // and allows you to yield null to skip a frame in EditMode
        [UnityTest]
        public IEnumerator TestWithEnumeratorPasses()
        {
            // RemoteComputation.Communicator.Initialize();
            Debug.Log("before load");
            SceneManager.LoadScene("Pendulum");
            Debug.Log("after load");
            yield return null;

            Debug.Log("after yield");

            var environment = Object.FindObjectOfType<Environment>();
            var pendulum = Object.FindObjectOfType<Pendulum>();
            var generator = new Generator();

            var generatedData = generator.Generate(0);

            // Setup stuff
            var state = environment.ResetEnvironment(generatedData);
            environment.RenderState(state);

            Debug.Log("before second yield");
            // Wait for the visual check of the correctness of setup
            yield return new WaitForSeconds(2f);

            Debug.Log("after wait");

            // Start training
            var dqnTask = MainController.ObtainModel<DQNPendulumActor>();

            var dqnActor = dqnTask.Result;
            Debug.Log(dqnTask.IsCompleted);

            Debug.Log(dqnActor);
        }
    }
}
