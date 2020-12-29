using System.Collections;
using Common;
using Common.ByteConversions;
using NUnit.Framework;
using RemoteComputation;
using RemoteComputation.Logging;
using Testing.TestCommon;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;
using LogOption = RemoteComputation.Logging.LogOption;

namespace Testing.PlayModeTests.Pendulum.Tests
{
    public abstract class PendulumFixture : CommunicatorFixture
    {
        protected StateRenderer stateRenderer;
        protected Environment environment;
        protected Pendulum pendulum;
        protected AdaptiveGenerator generator;
        protected DQNPendulumModel dqn;

        [UnitySetUp]
        public virtual IEnumerator SetUp()
        {
            yield return LoadScene();
            yield return ObtainDQN();

            generator   = new AdaptiveGenerator();
            environment = new Environment();
        }

        protected IEnumerator LoadScene()
        {
            SceneManager.LoadScene("Pendulum");

            yield return null;

            stateRenderer = Object.FindObjectOfType<StateRenderer>();
            pendulum      = Object.FindObjectOfType<Pendulum>();

            Assert.NotNull(stateRenderer);
            Assert.NotNull(pendulum);
        }

        protected IEnumerator ObtainDQN()
        {
            var dqnTask = MainController.ObtainModel<DQNPendulumModel>(Observation.SIZE.ToBytes(), Action.SIZE.ToBytes());
            yield return new WaitForTask(dqnTask);

            dqn = dqnTask.Result;

            Assert.NotNull(dqn);
        }

        protected IEnumerator SetLogOptions(params (LogOptionName optionName, LogOption optionValue)[] options)
        {
            yield return new WaitForTask(async () => {
                var logOptions = new LogOptions(options);
                await Communicator.Send(Message.SetLogOptions(dqn.Id, logOptions));
            });
        }
    }
}
