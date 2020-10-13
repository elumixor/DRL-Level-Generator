using System;
using System.Linq;
using AsyncIO;
using NetMQ;
using NetMQ.Sockets;

namespace PythonCommunication {
    public static class Communicator {
        const string ADDRESS = "tcp://localhost:5555";
        static bool isConnected;

        public static byte[] Compute(byte[] requestData) {
            client.SendFrame(requestData);

            var res = client.TryReceiveFrameBytes(new TimeSpan(0, 0, 1), out var message);
            if (!res)
                throw new Exception("Timeout. Backend unresponsive.");

            var header = (char) message[0];
            var data = message.Skip(1).ToArray();

            if (header == 'e') throw new Exception(System.Text.Encoding.ASCII.GetString(data));

            return data;
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
