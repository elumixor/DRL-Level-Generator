using NUnit.Framework;
using RemoteComputation;

namespace Testing.TestCommon
{
    [TestFixture]
    public class CommunicatorFixture : BaseFixture
    {
        [OneTimeSetUp] public virtual void OneTimeSetUp() { }

        [OneTimeTearDown] public virtual void OneTimeTearDown() { Communicator.Close(); }
    }
}
