using BackendCommunication;
using Common.ByteConversions;
using NUnit.Framework;

namespace Testing.EditorTests {
    public class CommunicationTest {
        const string ADDRESS = "tcp://localhost:5555";

        int testCount = 0;

        [SetUp] public void OpenConnection() => Communicator.OpenConnection(ADDRESS);

        [TearDown] public void CloseConnection() => Communicator.CloseConnection();

        [Test] public void EchoMessageWorks() {
            const string requestData = "hello вёрльд";
            var (bytes, startIndex) = Communicator.Send(RequestType.Echo, requestData.ToBytes());
            var responseString = bytes.GetString(startIndex).result;

            Assert.AreEqual(responseString, requestData);
        }
    }
}