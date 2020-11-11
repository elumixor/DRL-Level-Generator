using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading;
using NUnit.Framework;
using RL;
using RL.BackendCommunication;
using RL.Common.ByteConversions;
using RL.NN;

namespace Testing.EditorTests
{
    public class E2ESerializationTests
    {
        const string ADDRESS_SERVER = "tcp://*:5555";
        const string ADDRESS_CLIENT = "tcp://localhost:5555";

        static readonly Dictionary<string, string> args = new Dictionary<string, string> {{"address", ADDRESS_SERVER}};

        Process process;

        [SetUp]
        public void SetUp()
        {
            const string filePath = "tests/e2e_serialization/simple_serializer.py";
            process = ProcessRunner.CreateProcess(filePath, args, separateWindow: true);
            process.Start();
            Thread.Sleep(1000); // give some time to the process to launch
            Communicator.OpenConnection(ADDRESS_CLIENT);
        }

        [TearDown]
        public void TearDown()
        {
            Communicator.Send(RequestType.ShutDown);
            Communicator.CloseConnection();
            process.Close();
        }

        [Test]
        public void CanSerializeInt()
        {
            const int value = 5;
            var (response, startIndex) = SendToParse(value);

            Assert.AreEqual(startIndex + sizeof(int), response.Length);

            var reconstructed = response.ToInt(startIndex);
            Assert.AreEqual(value, reconstructed);
        }

        [Test]
        public void CanSerializeFloat()
        {
            const float value = 5.5f;
            var (response, startIndex) = SendToParse(value);

            Assert.AreEqual(startIndex + sizeof(float), response.Length);

            var reconstructed = response.ToFloat(startIndex);
            Assert.AreEqual(value, reconstructed);
        }

        [Test]
        public void CanSerializeString()
        {
            const string value = "hello world";
            var (response, startIndex) = SendToParse(value);

            var (reconstructed, bytesRead) = response.GetString(startIndex);
            Assert.AreEqual(value, reconstructed);
        }

        [Test]
        public void CanSerializeListInt()
        {
            var value = new[] {1, 2, 3};
            var (response, startIndex) = SendToParse(value);

            var (reconstructed, bytesRead) = response.GetListInt(startIndex);
            Assert.AreEqual(value, reconstructed);
        }

        [Test]
        public void CanSerializeListFloat()
        {
            var value = new float[] {1, 2, 3};
            var (response, startIndex) = SendToParse(value);

            var (reconstructed, bytesRead) = response.GetListFloat(startIndex);
            Assert.AreEqual(value, reconstructed);
        }

        [Test]
        public void CanSerializeTensor()
        {
            var tensor = new Tensor(new float[] {
                                            1, 2, 3, 4,
                                            5, 6,
                                    },
                                    new[] {2, 3});

            var (response, startIndex) = SendToParse(tensor);

            var (reconstructed, bytesRead) = response.Get<Tensor>(startIndex);
            Assert.AreEqual(tensor, reconstructed);
        }

        [Test]
        public void CanSerializeTensorRandom()
        {
            var tensor = new Linear(4, 5).StateDict.selfParameters[ModuleParameterName.weight];

            var (response, startIndex) = SendToParse(tensor);

            var (reconstructed, bytesRead) = response.Get<Tensor>(startIndex);
            Assert.AreEqual(tensor, reconstructed);
        }

        [Test]
        public void CanSerializeStateDict()
        {
            var stateDict = new Linear(4, 5).StateDict;

            var (response, startIndex) = SendToParse(stateDict);

            var (reconstructed, bytesRead) = response.Get<StateDict>(startIndex);
            Assert.AreEqual(stateDict, reconstructed);
        }

        [Test]
        public void CanSerializeStateDictComplex()
        {
            var sequential = new Sequential(new Sequential(new Linear(5, 4), new ReLU(), new Linear(4, 2)),
                                            new Sequential(new Linear(5, 4), new ReLU(), new Linear(4, 2)),
                                            new Linear(4, 2));
            var stateDict = sequential.StateDict;

            var (response, startIndex) = SendToParse(stateDict);

            var (reconstructed, bytesRead) = response.Get<StateDict>(startIndex);
            Assert.AreEqual(stateDict, reconstructed);
        }

        static (byte[] response, int startIndex) SendToParse(int data) => Communicator.Send(RequestType.Echo, "int".ToBytes().Concat(data.ToBytes()));

        static (byte[] response, int startIndex) SendToParse(float data) => Communicator.Send(RequestType.Echo, "float".ToBytes().Concat(data.ToBytes()));

        static (byte[] response, int startIndex) SendToParse(string data) => Communicator.Send(RequestType.Echo, "string".ToBytes().Concat(data.ToBytes()));

        static (byte[] response, int startIndex) SendToParse(IReadOnlyCollection<int> data) =>
                Communicator.Send(RequestType.Echo, "list_int".ToBytes().Concat(data.ToBytes(data.Count)));

        static (byte[] response, int startIndex) SendToParse(IReadOnlyCollection<float> data) =>
                Communicator.Send(RequestType.Echo, "list_float".ToBytes().Concat(data.ToBytes(data.Count)));

        static (byte[] response, int startIndex) SendToParse(Tensor data) => Communicator.Send(RequestType.Echo, "tensor".ToBytes().Concat(data.ToBytes()));

        static (byte[] response, int startIndex) SendToParse(StateDict data) =>
                Communicator.Send(RequestType.Echo, "state_dict".ToBytes().Concat(data.ToBytes()));
    }
}
