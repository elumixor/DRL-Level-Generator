using System.Collections.Generic;
using Common;

namespace Utilities {
    public class MemoryBuffer<TAction, TObservation> : IByteConvertible
        where TAction : IByteConvertible where TObservation : IByteConvertible {
        List<TObservation> observations = new List<TObservation>();
        List<TAction> actions = new List<TAction>();
        List<float> rewards = new List<float>();

        public void Clear() {
            observations = new List<TObservation>();
            actions = new List<TAction>();
            rewards = new List<float>();
        }

        public void Push(TObservation state, TAction action, float reward) {
            observations.Add(state);
            actions.Add(action);
            rewards.Add(reward);
        }

        public byte[] ToBytes() => ByteConverter.ConcatBytes(observations.ToBytes(), actions.ToBytes(), rewards.ToBytes());
    }
}