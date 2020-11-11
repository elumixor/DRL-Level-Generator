using System;
using System.Collections.Generic;
using System.Linq;
using AsyncIO;
using Common;
using Common.ByteConversions;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

namespace RemoteComputation
{
    public class Communicator : SingletonBehaviour<Communicator>
    {
        static bool isConnected;

        static PushSocket push;
        static PullSocket pull;

        static readonly Dictionary<int, Action<ByteReader>> Callbacks = new Dictionary<int, Action<ByteReader>>();

        static int currentId;
        static bool initialized;

        const int PUSH_PORT = 5671;
        const int PULL_PORT = 5672;

        /// <inheritdoc />
        protected override void Awake()
        {
            base.Awake();

            ForceDotNet.Force();

            push = new PushSocket();
            push.Connect($"tcp://localhost:{PUSH_PORT}");

            pull = new PullSocket();
            pull.Bind($"tcp://*:{PULL_PORT}");
        }

        static void CheckInstance()
        {
            if (instance == null) new GameObject("Communicator", typeof(Communicator));
        }

        public static void Close()
        {
            CheckInstance();

            push.Dispose();
            pull.Dispose();

            NetMQConfig.Cleanup();
        }

        public static void Send(IEnumerable<byte> data, Action<ByteReader> callback)
        {
            CheckInstance();

            Callbacks[currentId] = callback;
            push.SendFrame(currentId.ToBytes().ConcatMany(data).ToArray());
            currentId++;
        }

        public static void Send(string data, Action<ByteReader> callback)
        {
            CheckInstance();

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
}
