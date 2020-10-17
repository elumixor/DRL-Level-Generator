using Common.ByteConversions;
using DRL;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public class InferenceTransition : Transition<Action, State>, IByteConvertible {
        public InferenceTransition(State previousState, Action action, float reward, State nextState) : base(previousState, action, reward,
            nextState) { }

        public InferenceTransition(Transition<Action, State> transition) : base(transition.previousState, transition.action,
            transition.reward, transition.nextState) { }

        public byte[] ToBytes() =>
            ByteConverter.ConcatBytes(previousState.ToBytes(), action.ToBytes(), reward.ToBytes(), nextState.ToBytes());
    }
}