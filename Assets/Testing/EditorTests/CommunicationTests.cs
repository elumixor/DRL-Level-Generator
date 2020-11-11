using System.Collections.Generic;
using System.Threading;
using NUnit.Framework;
using RL;
using RL.BackendCommunication;
using RL.Common.ByteConversions;

namespace Testing.EditorTests
{
    [SingleThreaded]
    public class CommunicationTest
    {
        [Test]
        public void ServerInSeparateWindowWorks()
        {
            const string addressServer = "tcp://*:5555";
            const string addressClient = "tcp://localhost:5555";
            const string filePath = "tests/child_process/server_communication_test.py";
            var args = new Dictionary<string, string> {{"address", addressServer}};

            using (var p = ProcessRunner.CreateProcess(filePath, args, separateWindow: true)) {
                p.Start();
                Thread.Sleep(1000); // give some time to the process to launch
                Assert.False(p.HasExited);
                Communicator.OpenConnection(addressClient);
                var (responseBytes, startIndex) = Communicator.Send(RequestType.Echo, "echo".ToBytes());
                Assert.AreEqual("echo", responseBytes.GetString(startIndex).result);
                Communicator.Send(RequestType.Echo, "stop".ToBytes());
                Communicator.CloseConnection();
                Thread.Sleep(1000); // give some time to the process to exit
                Assert.True(p.HasExited);
                p.Close();
            }
        }
    }
}
