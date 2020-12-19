using System.Threading.Tasks;
using NUnit.Framework;
using RemoteComputation.Logging;
using Testing.TestCommon;

namespace Testing.PlayModeTests.Pendulum.Tests
{
    public class LoggingTests : CommunicatorFixture
    {
        [Test]
        public void DummyLogging()
        {
            Task.Run(async () => {
                     var model = await MainController.ObtainModel<DQNPendulumModel>();
                     var logOptions =
                             new LogOptions((LogOptionName.TrajectoryReward, new LogOption(10, 100, runningAverageSmoothing: 0.8f)));
                     await MainController.SetLogOptions(model, logOptions);
                 })
                .Wait(10000);
        }
    }
}
