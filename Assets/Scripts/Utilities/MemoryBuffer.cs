using System.Collections.Generic;
using Common;

namespace Utilities {
    public class MemoryBuffer<TAction, TObservation> : IByteConvertible
        where TAction : IByteConvertible where TObservation : IByteConvertible {
        CyclingQueue<TObservation> observations;
        CyclingQueue<TAction> actions;
        CyclingQueue<float> rewards;

        public MemoryBuffer(int size) {
            observations = new CyclingQueue<TObservation>(size);
            actions = new CyclingQueue<TAction>(size);
            rewards = new CyclingQueue<float>(size);
        }
        
        public int Length => observations.Length;

        public void Clear() {
            observations.Clear();
            actions.Clear();
            rewards.Clear();
        }

        public void Push(TObservation state, TAction action, float reward) {
            observations.Enqueue(state);
            actions.Enqueue(action);
            rewards.Enqueue(reward);
        }

        public byte[] ToBytes() =>
            ByteConverter.ConcatBytes(Length.ToBytes(), observations.ToBytes(), actions.ToBytes(), rewards.ToBytes());
    }
}