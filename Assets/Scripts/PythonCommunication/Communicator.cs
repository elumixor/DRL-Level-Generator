using System;
using System.Threading;
using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using TMPro;
using UnityEngine;

namespace PythonCommunication {
    public class Communicator : MonoBehaviour {
        static Thread listenerThread;

        static bool running = true;
        static string address = "tcp://localhost:5556";

        static bool shouldSendByteData;
        static byte[] byteData;

        static bool isConnected;

        public static Communicator Instance { get; private set; }
        public static event Action<byte[]> OnMessageReceived = delegate { };

        public static void SendMessage(byte[] data) {
            shouldSendByteData = true;
            byteData = data;
        }

        public static void OpenConnection() {
            if (isConnected) return;

            isConnected = true;

            listenerThread = new Thread(Instance.Listen);
            listenerThread.Start();
        }

        public static void CloseConnection() {
            if (!isConnected) return;

            isConnected = false;

            running = false;
            listenerThread.Join();
        }

        void Listen() {
            ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet

            using (var client = new RequestSocket()) {
                client.Connect(address);

                while (running) {
                    if (shouldSendByteData)
                        client.SendFrame(byteData);

                    if (client.TryReceiveFrameBytes(out var byteMessage))
                        OnMessageReceived(byteMessage);
                }
            }

            NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet
        }

        void Awake() => Instance = this;

        void OnDestroy() => CloseConnection();
    }
}