using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using AsyncIO;
using Common;
using Common.ByteConversions;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

namespace RemoteComputation
{
    public static class Communicator
    {
        static bool isConnected;

        static PushSocket push;
        static PullSocket pull;

        static readonly Dictionary<int, (object, ByteReader)> Callbacks = new Dictionary<int, (object, ByteReader)>();

        static int currentId;
        static bool initialized;

        const int PUSH_PORT = 5671;
        const int PULL_PORT = 5672;

        const int UPDATE_SLEEP_TIME = 50;

        static Task UpdateTask;
        static bool shouldExit;

        static object _lock = new object();

        static void CheckInstance()
        {
            if (initialized) return;

            ForceDotNet.Force();

            push = new PushSocket();
            push.Connect($"tcp://localhost:{PUSH_PORT}");

            pull = new PullSocket();
            pull.Bind($"tcp://*:{PULL_PORT}");

            UpdateTask  = new Task(CheckForUpdates);
            initialized = true;

            UpdateTask.Start();
        }

        public static void Close()
        {
            CheckInstance();

            shouldExit = true;
            UpdateTask.Wait();

            push.Dispose();
            pull.Dispose();

            NetMQConfig.Cleanup();
        }

        public static Task<ByteReader> Send(IEnumerable<byte> data)
        {
            return Task.Run(() => {
                var cond = new object();

                lock (_lock) {
                    CheckInstance();
                    Callbacks[currentId] = (cond, null);
                    push.SendFrame(currentId.ToBytes().ConcatMany(data).ToArray());
                    currentId++;
                }

                Monitor.Wait(cond);

                lock (_lock) {
                    var (_, byteReader) = Callbacks[currentId];
                    Callbacks.Remove(currentId);
                    return byteReader;
                }
            });
        }

        public static Task<ByteReader> Send(string data) => Send(data.ToBytes());
        public static Task<ByteReader> Send(Message data) => Send(data.Bytes);

        static void CheckForUpdates()
        {
            while (true) {
                lock (_lock) {
                    if (shouldExit) return;

                    if (Callbacks.Count == 0) continue;

                    // Get all messages
                    while (pull.TryReceiveFrameBytes(out var message)) {
                        var reader = new ByteReader(message);
                        var id = reader.ReadInt();

                        var (cond, _) = Callbacks[id];
                        Callbacks[id] = (cond, reader);

                        Monitor.Pulse(cond);
                    }
                }

                Thread.Sleep(UPDATE_SLEEP_TIME);
            }
        }
    }
}
