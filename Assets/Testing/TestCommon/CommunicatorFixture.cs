using System;
using NUnit.Framework;
using RemoteComputation;
using Testing.PlayModeTests.Common;
using UnityEngine;
using Object = UnityEngine.Object;

namespace Testing.TestCommon
{
    [TestFixture]
    public class CommunicatorFixture : BaseFixture
    {
        Breaker breaker;

        [OneTimeSetUp]
        public virtual void OneTimeSetUp()
        {
            breaker       =  new GameObject("Breaker").AddComponent<Breaker>();
            Breaker.Break += () => Assert.Fail("Broken");

            Object.DontDestroyOnLoad(breaker.gameObject);
        }

        [OneTimeTearDown] public virtual void OneTimeTearDown() { Object.Destroy(breaker.gameObject); }

        [TearDown] public virtual void TearDown() { Communicator.Close(); }
    }
}
