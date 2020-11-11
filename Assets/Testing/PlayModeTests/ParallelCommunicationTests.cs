using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using AsyncIO;
using Common;
using Common.ByteConversions;
using NetMQ;
using NetMQ.Sockets;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace Testing.PlayModeTests
{
    public class Communicator : SingletonBehaviour<Communicator>
    {
        static bool isConnected;

        static PushSocket push;
        static PullSocket pull;

        static readonly Dictionary<int, Action<ByteReader>> Callbacks = new Dictionary<int, Action<ByteReader>>();

        static int currentId = 0;

        public static void Initialize(int pushPort, int pullPort)
        {
            if (instance == null) new GameObject("Communicator", typeof(Communicator));

            ForceDotNet.Force();

            push = new PushSocket();
            push.Connect($"tcp://localhost:{pushPort}");

            pull = new PullSocket();
            pull.Bind($"tcp://*:{pullPort}");
        }

        public static void Close()
        {
            push.Dispose();
            pull.Dispose();

            NetMQConfig.Cleanup();
        }

        public static void Send(IEnumerable<byte> data, Action<ByteReader> callback)
        {
            Callbacks[currentId] = callback;
            push.SendFrame(currentId.ToBytes().ConcatMany(data).ToArray());
            currentId++;
        }

        public static void Send(string data, Action<ByteReader> callback)
        {
            Callbacks[currentId] = callback;
            push.SendFrame(currentId.ToBytes().ConcatMany(data.ToBytes()).ToArray());
            currentId++;
        }

        void Update()
        {
            // Wait until the message comes
            if (!pull.TryReceiveFrameBytes(out var message)) return;

            var reader = new ByteReader(message);
            var id = reader.ReadInt();
            Callbacks[id](reader);
            Callbacks.Remove(id);
        }
    }

    public class ParallelCommunicationTests
    {
        [SetUp] public void SetUp() { Communicator.Initialize(5671, 5672); }

        [TearDown] public void TearDown() { Communicator.Close(); }

        [UnityTest]
        public IEnumerator SendingAndReceivingDataNonBlocking()
        {
            var resolved1 = false;
            var resolved2 = false;

            // T1
            // send request
            Communicator.Send("ready 1",
                              delegate {
                                  Debug.Log("Done 1");
                                  resolved1 = true;
                              });

            // T2
            // send request
            Communicator.Send("Done 1",
                              delegate {
                                  Debug.Log("Done 2");
                                  resolved2 = true;
                              });

            // T1
            // get response

            // T2
            // get response
            yield return new WaitUntil(() => resolved1 && resolved2);
        }
    }
}
