using Common.ByteConversions;
using DRL;
using Implementation.Dummy;

namespace Training_Setups.Pendulum.Scripts.DRL {
    public class InferenceTransition : Transition<DummyAction, State>, IByteConvertible {
        public InferenceTransition(State previousState, DummyAction action, float reward, State nextState) : base(previousState, action,
            reward, nextState) { }

        public InferenceTransition(Transition<DummyAction, State> transition) : base(transition.previousState, transition.action,
            transition.reward, transition.nextState) { }

        public byte[] ToBytes() =>
            ByteConverter.ConcatBytes(previousState.ToBytes(), action.ToBytes(), reward.ToBytes(), nextState.ToBytes());
    }
}