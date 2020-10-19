using System.Collections.Generic;
using Common;
using Common.ByteConversions;
using DRL;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public class InferenceTransition : Transition<Action, State>, IByteConvertible {
        public InferenceTransition(Transition<Action, State> transition) : base(transition.previousState, transition.action,
                                                                                transition.reward, transition.nextState) { }

        public IEnumerable<byte> ToBytes() => previousState.ToBytes().ConcatMany(action.ToBytes(), reward.ToBytes(), nextState.ToBytes());
    }
}