using System.Collections;
using System.Threading.Tasks;
using Common.ByteConversions;
using RemoteComputation.Logging;
using Testing.TestCommon;
using UnityEngine;
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
        }
    }
}
