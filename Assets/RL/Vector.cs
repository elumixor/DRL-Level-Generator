using System;
using System.Collections;
using System.Collections.Generic;
using Common.ByteConversions;

namespace RL
{
    public class Vector : ObservableState<Vector>, IEnumerable<float>, IByteConvertible
    {
        protected readonly float[] values;

        public Vector(params float[] values) => this.values = values;

        public float this[int i] => values[i];

        /// <inheritdoc/>
        public IEnumerator<float> GetEnumerator() => ((IEnumerable<float>) values).GetEnumerator();

        /// <inheritdoc/>
        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

        /// <inheritdoc/>
        public IEnumerable<byte> Bytes => values.ToBytes(values.Length);

        public static implicit operator Vector(float value) => new Vector(value);

        /// <inheritdoc/>
        public override Vector Observation => this;

        public override bool Equals(object obj)
        {
            if (obj is Vector v2) {
                if (v2.values.Length != values.Length) return false;

                for (var i = 0; i < values.Length; i++)
                    if (Math.Abs(v2.values[i] - values[i]) > 1e-7f)
                        return false;

                return true;
            }

            return false;
        }
    }
}
