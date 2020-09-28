using AsyncIO;
using NetMQ;
using NetMQ.Sockets;

namespace PythonCommunication {
    public static class Communicator {
        const string ADDRESS = "tcp://localhost:5555";
        static bool isConnected;

        public static byte[] Compute(byte[] data) {
            client.SendFrame(data);
            var receiveFrameBytes = client.ReceiveFrameBytes();
            return receiveFrameBytes;
        }

        static RequestSocket client;

        public static void OpenConnection() {
            if (isConnected) return;
            ForceDotNet.Force();

            isConnected = true;

            client = new RequestSocket();
            client.Connect(ADDRESS);
        }

        public static void CloseConnection() {
            if (!isConnected) return;

            isConnected = false;

            client.Dispose();
            NetMQConfig.Cleanup();
        }
    }
}