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

namespace RemoteComputation
{
    public static class Communicator
    {
        static bool isConnected;

        static PushSocket push;
        static PullSocket pull;

        static readonly Dictionary<int, (SemaphoreSlim, ByteReader)> Callbacks = new Dictionary<int, (SemaphoreSlim, ByteReader)>();

        static int currentId;
        static bool initialized;

        const int PUSH_PORT = 5671;
        const int PULL_PORT = 5672;

        const int UPDATE_SLEEP_TIME = 50;

        static Task UpdateTask;
        static bool shouldExit;

        static readonly SemaphoreSlim semaphore = new SemaphoreSlim(1, 1);

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
                var cond = new SemaphoreSlim(0, 1);

                semaphore.Wait();

                CheckInstance();
                var id = currentId;
                Callbacks[id] = (cond, null);
                push.SendFrame(id.ToBytes().ConcatMany(data).ToArray());
                currentId++;

                semaphore.Release();

                cond.Wait();

                semaphore.Wait();

                var (_, byteReader) = Callbacks[id];
                Callbacks.Remove(id);
                semaphore.Release();
                return byteReader;
            });
        }

        public static Task<ByteReader> Send(string data) => Send(data.ToBytes());
        public static Task<ByteReader> Send(Message data) => Send(data.Bytes);

        static void CheckForUpdates()
        {
            while (true) {
                semaphore.Wait();

                if (shouldExit) return;

                if (Callbacks.Count == 0) continue;

                // Get all messages
                while (pull.TryReceiveFrameBytes(out var message)) {
                    Console.WriteLine($"received! {message}");
                    var reader = new ByteReader(message);
                    var id = reader.ReadInt();

                    var (cond, _) = Callbacks[id];
                    Callbacks[id] = (cond, reader);

                    cond.Release();
                }

                semaphore.Release();

                Thread.Sleep(UPDATE_SLEEP_TIME);
            }
        }
    }
}
