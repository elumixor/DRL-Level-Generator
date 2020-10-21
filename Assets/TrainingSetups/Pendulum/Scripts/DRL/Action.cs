using System.Collections;
using System.Collections.Generic;
using System.Linq;
using Common.ByteConversions;
using Serialization;

namespace TrainingSetups.Pendulum.Scripts.DRL {
    public readonly struct Action : IByteConvertible, IEnumerable<float> {
        [Structural]
        public float FloatValue => tap ? 1f : -1f;

        public readonly bool tap;

        public Action(IEnumerable<float> result) {
            var value = result.First();
            tap = value > 0;
        }

        public IEnumerable<byte> ToBytes() => FloatValue.ToBytes();
        public IEnumerator<float> GetEnumerator() { yield return FloatValue; }
        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
    }
}