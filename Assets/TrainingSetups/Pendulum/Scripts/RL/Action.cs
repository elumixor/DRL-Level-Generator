using System.Collections;
using System.Collections.Generic;
using Common.ByteConversions;
using Serialization;

namespace TrainingSetups.Pendulum.Scripts.RL {
    public readonly struct Action : IByteConvertible, IEnumerable<float> {
        [Structural]
        public float FloatValue => tap ? 1 : 0;

        public readonly bool tap;

        public Action(int result) => tap = result > 0;

        public IEnumerable<byte> ToBytes() => FloatValue.ToBytes();
        public IEnumerator<float> GetEnumerator() { yield return FloatValue; }
        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
    }
}