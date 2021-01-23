using System;
using System.Threading.Tasks;
using Common.ByteConversions;
using NUnit.Framework;
using RemoteComputation;
using RemoteComputation.Logging;
using Testing.TestCommon;

namespace Testing.EditorTests
{
    public class CommunicationTestsNoUnity : CommunicatorFixture
    {
        [Test]
        public void TestCommunication()
        {
            var task = Communicator.Send(Message.Test(5.ToBytes()));
            task.Wait();
            var result = task.Result;
            Console.WriteLine(result);
            Assert.AreEqual(result.ReadInt(), 5);
        }

        [Test]
        public void TestLogging()
        {
            var o = TestContext.Out;
            o.WriteLine("a");

            var t = Task.Run(async () => {
                await o.WriteLineAsync("anything...");
                var model = await MainController.ObtainModel<DQN>(5.ToBytes(), 7.ToBytes());
                o.WriteLine(model);
                var logOptions = new LogOptions((LogOptionName.TrajectoryReward, new LogOption(10, 100, runningAverageSmoothing: 0.8f)));
                await MainController.SetLogOptions(model, logOptions);
                await o.WriteLineAsync("Good!");
            });
            o.WriteLine("b");

            if (!t.Wait(5000)) {
                o.WriteLine("?");
                Assert.Fail("Too slow");
            }

            o.WriteLine("c");
        }
    }
}
