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

        public static (byte[] response, ResponseType responseType, int startIndex) Send(
            string requestMessage, IEnumerable<byte> requestData) {
            var bytes = requestMessage.ToBytes().Concat(requestData).ToArray();
            client.SendFrame(bytes);

            var res = client.TryReceiveFrameBytes(new TimeSpan(0, 0, 1), out var response);
            if (!res)
                throw new Exception("Timeout. Backend unresponsive.");

            var (responseTypeString, bytesRead) = response.GetString();

            if (!Enum.TryParse(responseTypeString, out ResponseType responseType))
                throw new Exception($"Backend send in invalid response message: {responseTypeString}");

            if (responseType == ResponseType.Failure)
                throw new Exception($"Failure on backend: {response.GetString(bytesRead).result}");

            return (response, responseType, bytesRead);
        }

        public static (byte[]response, ResponseType responseType, int startIndex) Send(
            RequestType requestType, IEnumerable<byte> requestData) => Send(requestType.ToString(), requestData);


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