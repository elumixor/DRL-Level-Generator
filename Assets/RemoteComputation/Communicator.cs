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
    public class Communicator
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

        static Task updateTask;
        static bool shouldExit;

        static readonly SemaphoreSlim Semaphore = new SemaphoreSlim(1, 1);

        static void Initialize()
        {
            Semaphore.Wait();

            if (initialized) {
                Semaphore.Release();
                return;
            }

            shouldExit = false;

            ForceDotNet.Force();

            push = new PushSocket();
            pull = new PullSocket();

            push.Connect($"tcp://localhost:{PUSH_PORT}");
            pull.Bind($"tcp://*:{PULL_PORT}");

            updateTask = Task.Run(CheckForUpdates);

            initialized = true;

            Semaphore.Release();
        }

        public static void Close()
        {
            Semaphore.Wait();

            if (!initialized) {
                Semaphore.Release();
                return;
            }

            shouldExit = true;

            Semaphore.Release();

            updateTask.Wait();

            Semaphore.Wait();

            push.Dispose();
            pull.Dispose();

            NetMQConfig.Cleanup();

            // todo: release all the semaphores for the waiting conditions
            // todo: throw some error if there is one

            initialized = false;

            Semaphore.Release();
        }

        public static Task<ByteReader> Send(IEnumerable<byte> data)
        {
            Initialize();

            return Task.Run(() => {
                Semaphore.Wait();

                var id = currentId;
                var cond = new SemaphoreSlim(0, 1);

                Callbacks[id] = (cond, null);

                push.SendFrame(id.ToBytes().ConcatMany(data).ToArray());

                currentId++;

                Semaphore.Release();

                cond.Wait();

                Semaphore.Wait();

                var (_, byteReader) = Callbacks[id];

                Callbacks.Remove(id);

                Semaphore.Release();

                return byteReader;
            });
        }

        public static Task<ByteReader> Send(string data) => Send(data.ToBytes());
        public static Task<ByteReader> Send(Message data) => Send(data.Bytes);

        static void CheckForUpdates()
        {
            Semaphore.Wait();

            while (true) {
                if (shouldExit) {
                    Semaphore.Release();
                    return;
                }

                if (Callbacks.Count == 0) {
                    Semaphore.Release();
                    Thread.Sleep(UPDATE_SLEEP_TIME);
                    Semaphore.Wait();
                    continue;
                }

                // Get all messages
                while (pull.TryReceiveFrameBytes(out var message)) {
                    var reader = new ByteReader(message);
                    var id = reader.ReadInt();

                    var (cond, _) = Callbacks[id];
                    Callbacks[id] = (cond, reader);

                    cond.Release();
                }

                Semaphore.Release();
                Thread.Sleep(UPDATE_SLEEP_TIME);
                Semaphore.Wait();
            }
        }
    }
}
