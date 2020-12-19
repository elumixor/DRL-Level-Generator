using NUnit.Framework;
using RemoteComputation;

namespace Testing.TestCommon
{
    public class CommunicatorFixture : BaseFixture
    {
        [TearDown] public virtual void TearDown() { Communicator.Close(); }
    }
}
