using System.Collections.Generic;
using Common;

namespace Utilities {
    public class MemoryBuffer<TAction, TState> : IByteConvertible
        where TAction : IByteConvertible where TState : IByteConvertible {
        CyclingQueue<TState> states;
        CyclingQueue<TAction> actions;
        CyclingQueue<float> rewards;

        public MemoryBuffer(int size) {
            states = new CyclingQueue<TState>(size);
            actions = new CyclingQueue<TAction>(size);
            rewards = new CyclingQueue<float>(size);
        }
        
        public int Length => states.Length;

        public void Clear() {
            states.Clear();
            actions.Clear();
            rewards.Clear();
        }

        public void Push(TState state, TAction action, float reward) {
            states.Push(state);
            actions.Push(action);
            rewards.Push(reward);
        }

        public byte[] ToBytes() =>
            ByteConverter.ConcatBytes(Length.ToBytes(), states.ToBytes(), actions.ToBytes(), rewards.ToBytes());
    }
}