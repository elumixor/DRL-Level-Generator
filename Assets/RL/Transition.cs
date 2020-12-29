using System.Collections.Generic;
using Common;
using Common.ByteConversions;

namespace RL
{
    public readonly struct Transition<TState, TAction, TObservation> : IByteConvertible
            where TState : ObservableState<TObservation>, IByteConvertible
            where TAction : Vector
            where TObservation : Vector
    {
        public readonly TState state;
        public readonly TAction action;
        public readonly float reward;
        public readonly TState nextState;

        public Transition(TState state, TAction action, float reward, TState nextState)
        {
            this.state     = state;
            this.action    = action;
            this.reward    = reward;
            this.nextState = nextState;
        }

        public IEnumerable<byte> Bytes => state.Bytes.ConcatMany(action.Bytes, reward.ToBytes(), nextState.Bytes);
    }

    public readonly struct Transition
    {
        public readonly Vector state;
        public readonly Vector action;
        public readonly float reward;
        public readonly Vector nexVector;

        public Transition(Vector state, Vector action, float reward, Vector nexVector)
        {
            this.state     = state;
            this.action    = action;
            this.reward    = reward;
            this.nexVector = nexVector;
        }

        public IEnumerable<byte> Bytes => state.Bytes.ConcatMany(action.Bytes, reward.ToBytes(), nexVector.Bytes);
    }
}
