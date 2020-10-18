using System;
using System.Collections.Generic;
using System.Linq;
using AsyncIO;
using Common.ByteConversions;
using NetMQ;
using NetMQ.Sockets;

namespace BackendCommunication {
    public static class Communicator {
        static bool isConnected;
        static RequestSocket client;

        static readonly IEnumerable<byte> EmptyBytes = Enumerable.Empty<byte>();

        public static (byte[] response, int startIndex) Send(string requestMessage, IEnumerable<byte> requestData = null) {
            var bytes = requestMessage.ToBytes().Concat(requestData ?? EmptyBytes).ToArray();
            client.SendFrame(bytes);

            var res = client.TryReceiveFrameBytes(new TimeSpan(0, 0, 1), out var response);
            if (!res)
                throw new CommunicationException("Timeout. Backend unresponsive.");

            var (responseTypeString, bytesRead) = response.GetString();

            if (!Enum.TryParse(responseTypeString, out ResponseType responseType))
                throw new CommunicationException($"Backend send in invalid response message: {responseTypeString}");

            if (responseType == ResponseType.Failure)
                throw new CommunicationException($"Failure on backend: {response.GetString(bytesRead).result}");

            return (response, bytesRead);
        }

        public static (byte[]response, int startIndex) Send(RequestType requestType, IEnumerable<byte> requestData = null) =>
            Send(requestType.ToString(), requestData);


        public static void OpenConnection(string address) {
            if (isConnected) return;
            ForceDotNet.Force();

            isConnected = true;

            client = new RequestSocket();
            client.Connect(address);
        }

        public static void CloseConnection() {
            if (!isConnected) return;

            isConnected = false;

            client.Dispose();
            NetMQConfig.Cleanup();
        }
    }
}