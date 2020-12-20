using System.Collections;
using System.Threading.Tasks;
using Common.ByteConversions;
using Common.RandomValues;
using NUnit.Framework;
using RemoteComputation.Logging;
using Testing.TestCommon;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;
using LogOption = RemoteComputation.Logging.LogOption;

namespace Testing.PlayModeTests.Pendulum.Tests
{
    public class LoggingTests : CommunicatorFixture
    {
        [UnityTest]
        public IEnumerator DummyLogging()
        {
            var t = Task.Run(async () => {
                var model = await MainController.ObtainModel<DQNPendulumModel>(5.ToBytes(), 7.ToBytes());
                var logOptions = new LogOptions((LogOptionName.TrajectoryReward, new LogOption(10, 100, runningAverageSmoothing: 0.8f)));
                await MainController.SetLogOptions(model, logOptions);
                Debug.Log("Yay");
            });

            yield return new WaitForSeconds(10);

            if (!t.IsCompleted) Assert.Fail("Nay");
        }

        [UnityTest]
        public IEnumerator TrainingLoggingWorks()
        {
            SceneManager.LoadScene("Pendulum");
            yield return null;

            var environment = Object.FindObjectOfType<Environment>();
            var pendulum = Object.FindObjectOfType<Pendulum>();
            var generator = new Generator(new UniformValueInt(2, 3),
                                          new UniformValue(0.5f, 0.5f),
                                          new UniformValue(-1, 1),
                                          new UniformValue(1f, 2f));

            var generatedData = generator.Generate(0);

            // Setup stuff
            var state = environment.ResetEnvironment(generatedData);
            environment.RenderState(state);

            Debug.Log("Set Up Done");
            yield return null;

            // Start training

            var dqnTask = MainController.ObtainModel<DQNPendulumModel>(State.SIZE.ToBytes(), Action.SIZE.ToBytes());
            yield return new WaitUntil(() => dqnTask.IsCompleted);

            Assert.IsTrue(dqnTask.IsCompleted);

            var dqnModel = dqnTask.Result;

            var trainingTask = MainController.TrainAgent(dqnModel,
                                                         generator,
                                                         0.5f,
                                                         dqnModel,
                                                         environment,
                                                         10,
                                                         10,
                                                         new LogOptions((LogOptionName.TrajectoryReward,
                                                                         new LogOption(10, 100, runningAverageSmoothing: 0.8f))));
        }
    }
}
