using System;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using AsyncIO;
using Common;
using Common.ByteConversions;
using NetMQ;
using NetMQ.Sockets;
using NUnit.Framework;
using RemoteComputation;
using UnityEngine;

namespace Testing.EditorTests
{
    public class CommunicationTest
    {
        readonly SemaphoreSlim ss = new SemaphoreSlim(0, 1);

        Task T1()
        {
            return Task.Run(() => {
                Console.WriteLine("Start 1");
                Thread.Sleep(1000);
                ss.Release();
                Console.WriteLine("End 1");
            });
        }

        Task WaitsOnT1()
        {
            return Task.Run(() => {
                Console.WriteLine("Start 2");
                Thread.Sleep(500);
                Console.WriteLine("Sleep ended 2");

                Console.WriteLine("Before wait");
                ss.Wait();
                Console.WriteLine("After wait");

                Console.WriteLine("End 2");
            });
        }

        [Test]
        public void LockingTest()
        {
            Console.WriteLine("?");
            var t1 = T1();
            var t2 = WaitsOnT1();
            t1.Wait();
            t2.Wait();
            Console.WriteLine("Finished");
        }

        [Test]
        public void TestCommunication()
        {
            var task = Communicator.Send(Message.Test(5.ToBytes()));
            task.Wait();
            Debug.Log(task.Result.ReadInt());
            Communicator.Close();
        }

        [Test]
        public void TestFreezingWithUsing()
        {
            ForceDotNet.Force();

            using (var push = new PushSocket()) {
                push.Connect($"tcp://localhost:{5671}");

                using (var pull = new PullSocket()) { pull.Bind($"tcp://*:{5672}"); }
            }

            NetMQConfig.Cleanup();
        }

        [Test]
        public void TestFreezingWithoutUsing()
        {
            ForceDotNet.Force();

            // {
            var push = new PushSocket();
            push.Connect($"tcp://localhost:{5671}");

            var pull = new PullSocket();
            pull.Bind($"tcp://*:{5672}");

            push.Dispose();
            pull.Dispose();
            // }

            NetMQConfig.Cleanup();
        }

        [Test]
        public void DummySend()
        {
            ForceDotNet.Force();

            var push = new PushSocket();
            var pull = new PullSocket();

            push.Connect($"tcp://localhost:{5671}");
            pull.Bind($"tcp://*:{5672}");

            var messageBytes = Message.Test(5.ToBytes()).Bytes;

            push.SendFrame(0.ToBytes().ConcatMany(messageBytes).ToArray());
            var response = pull.ReceiveFrameBytes();

            Debug.Log(response);

            push.Dispose();
            pull.Dispose();

            NetMQConfig.Cleanup();
        }

        [Test]
        public void DummySendWithTasks()
        {
            // Send 5 times, receive 5 times
            ForceDotNet.Force();

            var push = new PushSocket();
            var pull = new PullSocket();

            push.Connect($"tcp://localhost:{5671}");
            pull.Bind($"tcp://*:{5672}");

            try {
                var t1 = Task.Run(() => {
                    for (var i = 0; i < 5; i++) {
                        var messageBytes = Message.Test(i.ToBytes()).Bytes;
                        push.SendFrame(i.ToBytes().ConcatMany(messageBytes).ToArray());
                        Debug.Log($"Sent {i}");
                        Thread.Sleep(500);
                    }
                });

                var t2 = Task.Run(() => {
                    for (var i = 0; i < 5; i++) {
                        var response = pull.ReceiveFrameBytes();
                        var reader = new ByteReader(response);
                        Debug.Log($"message id: {reader.ReadInt()} data: {reader.ReadInt()}");
                    }
                });

                t1.Wait();
                t2.Wait();
            } catch (Exception e) { Debug.LogException(e); }

            push.Dispose();
            pull.Dispose();

            NetMQConfig.Cleanup();
        }
    }
}
