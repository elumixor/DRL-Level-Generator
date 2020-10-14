using System;
using System.Collections;
using NUnit.Framework;
using UnityEngine.TestTools;

namespace Testing.StaticTests
{
    public class SerializationTests
    {
        // A Test behaves as an ordinary method
        [Test]
        public void SerializationTestSimplePasses()
        {
            // Use the Assert class to test conditions
            Assert.That(1 == 2, "Fail this test");
        }

        // A UnityTest behaves like a coroutine in Play Mode. In Edit Mode you can use
        // `yield return null;` to skip a frame.
        [UnityTest]
        public IEnumerator SerializationTestWithEnumeratorPasses()
        {
            // Use the Assert class to test conditions.
            // Use yield to skip a frame.
            Console.WriteLine("this is a test output");
            yield return null;
        }
    }
}
