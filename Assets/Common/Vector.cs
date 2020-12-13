using System.Collections;
using System.Collections.Generic;
using Common.ByteConversions;

namespace Common
{
    public class Vector : IEnumerable<float>, IByteConvertible
    {
        protected readonly float[] values;

        public Vector(params float[] values) { this.values = values; }

        /// <inheritdoc/>
        public IEnumerator<float> GetEnumerator() => ((IEnumerable<float>) values).GetEnumerator();

        /// <inheritdoc/>
        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

        /// <inheritdoc/>
        public IEnumerable<byte> Bytes => values.ToBytes(values.Length);

        public static implicit operator Vector(float value) => new Vector(value);
    }
}
