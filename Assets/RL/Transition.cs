using System.Collections.Generic;
using System.Linq;
using Common;
using Common.ByteConversions;

namespace RL
{
    public readonly struct Transition : IByteConvertible
    {
        public readonly Vector state;
        public readonly Vector action;
        public readonly float reward;
        public readonly Vector nextState;

        public Transition(Vector state, Vector action, float reward, Vector nextState)
        {
            this.state     = state;
            this.action    = action;
            this.reward    = reward;
            this.nextState = nextState;
        }

        public IEnumerable<byte> Bytes => state.Bytes.ConcatMany(action.ToBytes(), reward.ToBytes(), nextState.Bytes);
    }
}
