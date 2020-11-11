using System;
using System.Collections.Generic;
using System.Linq;
using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using RL.Common.ByteConversions;

namespace RL.BackendCommunication
{
    public static class Communicator
    {
        static bool isConnected;
        static RequestSocket client;

        static readonly IEnumerable<byte> EmptyBytes = Enumerable.Empty<byte>();

        static (byte[] response, int startIndex) Send(string requestMessage, IEnumerable<byte> requestData, int timeout)
        {
            var bytes = requestMessage.ToBytes().Concat(requestData ?? EmptyBytes).ToArray();
            client.SendFrame(bytes);

            bool res;
            byte[] response;
            res = timeout <= 0
                          ? client.TryReceiveFrameBytes(new TimeSpan(0, 0, 10), out response)
                          : client.TryReceiveFrameBytes(new TimeSpan(0, 0, 0, 0, timeout), out response);

            if (!res) throw new CommunicationException("Timeout. Backend unresponsive.");

            var (responseTypeString, bytesRead) = response.GetString();

            if (!Enum.TryParse(responseTypeString, out ResponseType responseType))
                throw new CommunicationException($"Backend send in invalid response message: {responseTypeString}");

            if (responseType == ResponseType.Failure) throw new CommunicationException($"Failure on backend: {response.GetString(bytesRead).result}");

            return (response, bytesRead);
        }

        /// <param name="timeout"> Milliseconds </param>
        public static (byte[]response, int startIndex) Send(RequestType requestType, IEnumerable<byte> requestData = null, int timeout = 1000) =>
                Send(requestType.ToString(), requestData, timeout);

        public static void OpenConnection(string address)
        {
            if (isConnected) return;

            ForceDotNet.Force();

            isConnected = true;

            client = new RequestSocket();
            client.Connect(address);
        }

        public static void CloseConnection()
        {
            if (!isConnected) return;

            isConnected = false;

            client.Dispose();
            NetMQConfig.Cleanup();
        }
    }
}
