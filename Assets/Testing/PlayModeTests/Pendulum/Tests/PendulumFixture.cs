using System.Collections;
using Common;
using Common.ByteConversions;
using NUnit.Framework;
using RemoteComputation;
using RemoteComputation.Logging;
using RL;
using Testing.TestCommon;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;
using LogOption = RemoteComputation.Logging.LogOption;

namespace Testing.PlayModeTests.Pendulum.Tests
{
    public abstract class PendulumFixture<TGenerator, TStateRenderer> : CommunicatorFixture
            where TGenerator : MonoBehaviour, IGenerator<GeneratedData>
            where TStateRenderer : MonoBehaviour, IStateRenderer<State, GeneratedData>
    {
        protected TStateRenderer stateRenderer;
        protected Environment environment;
        protected Pendulum pendulum;
        protected TGenerator generator;
        protected DQNPendulumModel dqn;

        [UnitySetUp]
        public virtual IEnumerator SetUp()
        {
            yield return LoadScene();
            yield return ObtainDQN();

            environment = new Environment();
        }

        protected IEnumerator LoadScene()
        {
            SceneManager.LoadScene("Pendulum");

            yield return null;

            stateRenderer = Object.FindObjectOfType<TStateRenderer>();
            pendulum      = Object.FindObjectOfType<Pendulum>();
            generator     = Object.FindObjectOfType<TGenerator>();

            Assert.NotNull(stateRenderer);
            Assert.NotNull(pendulum);
            Assert.NotNull(generator);
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
