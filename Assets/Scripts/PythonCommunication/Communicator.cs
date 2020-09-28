using System;
using System.Threading;
using System.Threading.Tasks;
using AsyncIO;
using Common;
using NetMQ;
using NetMQ.Sockets;
using UnityEditor;
using UnityEngine;

namespace PythonCommunication {
    public class Communicator {
        static Thread listenerThread;
        static bool running = true;
        const string ADDRESS = "tcp://localhost:5555";
        static bool shouldSendByteData;
        static byte[] byteData;
        static bool isConnected;

        public static event Action<byte[]> OnMessageReceived = delegate { };

        public static void SendMessage(byte[] data) {
            shouldSendByteData = true;
            byteData = data;
        }

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
            // listenerThread = new Thread(Listen);
            // listenerThread.Start();
        }

        public static void CloseConnection() {
            if (!isConnected) return;

            isConnected = false;

            client.Dispose();
            NetMQConfig.Cleanup();
            listenerThread.Join();
        }

        static void Listen() {
            // // this line is needed to prevent unity freeze after one use, not sure why yet
            //
            // var 
            //
            // using (var client = new RequestSocket()) {
            //     client.Connect(ADDRESS);
            //
            //     while (running) {
            //         if (shouldSendByteData) {
            //             client.SendFrame(byteData);
            //             shouldSendByteData = false;
            //
            //             if (client.TryReceiveFrameBytes(out var byteMessage))
            //                 OnMessageReceived(byteMessage);
            //         }
            //     }
            // }

            // this line is needed to prevent unity freeze after one use, not sure why yet
        }
    }
}