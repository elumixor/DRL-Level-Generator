using System.Collections.Generic;
using System.Linq;
using System.Runtime.Remoting;
using System.Threading;
using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using NUnit.Framework;
using UnityEngine;
using Random = System.Random;

namespace Testing.EditorTests
{
    [SingleThreaded]
    public class CommunicationTest
    {
        const string addressServer = "tcp://*:5555";
        const string addressClient = "tcp://localhost:5555";
        const string filePath = "tests/child_process/server_communication_test.py";

        // [Test]
        // public void ServerInSeparateWindowWorks()
        // {
        //     var args = new Dictionary<string, string> {{"address", addressServer}};
        //
        //     using (var p = ProcessRunner.CreateProcess(filePath, args, separateWindow: true)) {
        //         p.Start();
        //         Thread.Sleep(1000); // give some time to the process to launch
        //         Assert.False(p.HasExited);
        //         Communicator.OpenConnection(addressClient);
        //         var (responseBytes, startIndex) = Communicator.Send(RequestType.Echo, "echo".ToBytes());
        //         Assert.AreEqual("echo", responseBytes.GetString(startIndex).result);
        //         Communicator.Send(RequestType.Echo, "stop".ToBytes());
        //         Communicator.CloseConnection();
        //         Thread.Sleep(1000); // give some time to the process to exit
        //         Assert.True(p.HasExited);
        //         p.Close();
        //     }
        // }

        /// <summary>
        /// The tests shows how we do non-blocking receiving: on each update frame we can
        /// check whether the response is received (via) TryReceive...
        /// </summary>
        [Test]
        public void AsyncClientsTest()
        {
            ForceDotNet.Force();
            var r = new Random();

            var client = new RequestSocket();
            client.Connect("tcp://127.0.0.1:5671");

            var total = 0;

            client.ReceiveReady += (sender, args) => Debug.Log("Ready");

            while (true) {
                client.SendFrame("ready");

                string msg;

                while (!client.TryReceiveFrameString(out msg)) {
                    // Debug.Log("still waiting");
                }

                Debug.Log(msg);

                if (msg == "END") break;

                total++;
            }

            Debug.Log($"Received {total}");


            client.Dispose();
            NetMQConfig.Cleanup();
        }
    }
}
