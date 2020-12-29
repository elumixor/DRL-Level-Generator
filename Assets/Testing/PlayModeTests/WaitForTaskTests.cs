using System.Collections;
using System.Threading;
using Common;
using Common.ByteConversions;
using NUnit.Framework;
using RemoteComputation;
using Testing.TestCommon;
using UnityEngine;
using UnityEngine.TestTools;

namespace Testing.PlayModeTests
{
    public class WaitForTaskTests : CommunicatorFixture
    {
        [UnityTest]
        public IEnumerator TestWaitingForTask()
        {
            Debug.Log("Stating");

            yield return new WaitForTask(() => {
                Debug.Log("Task Started");
                Thread.Sleep(1000);
                Debug.Log("After 1 second");
                Thread.Sleep(1000);
                Debug.Log("After 2 seconds. Ending");
            });

            Debug.Log("After wait");
        }

        [UnityTest]
        public IEnumerator TestForCommunicatorResponse()
        {
            var task = Communicator.Send(Message.Test(5.ToBytes()));
            yield return new WaitForTask(task);

            var result = task.Result;

            Assert.AreEqual(result.ReadInt(), 5);
        }

        [UnityTest]
        public IEnumerator TestForCommunicatorResponseLambda()
        {
            ByteReader result = default;
            yield return new WaitForTask(async () => result = await Communicator.Send(Message.Test(5.ToBytes())));

            Assert.AreEqual(result.ReadInt(), 5);
        }

        [UnityTest]
        public IEnumerator TestClosure()
        {
            var hello = "hello";

            yield return new WaitForTask(() => { hello = "world"; });

            Assert.AreEqual(hello, "world");
        }
    }
}
