using System.Collections;
using System.Collections.Generic;
using System.Linq;
using Common;
using Common.ByteConversions;
using Serialization;
using UnityEngine;

namespace TrainingSetups.Pendulum.Scripts.DRL {
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