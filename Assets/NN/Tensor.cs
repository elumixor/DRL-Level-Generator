using System.Collections.Generic;
using System.Linq;
using Common;
using Common.ByteConversions;

namespace NN
{
    public struct Tensor : IByteSerializable
    {
        public float[] data;
        public int[] shape;

        public Tensor(float[] data, int[] shape)
        {
            this.data  = data;
            this.shape = shape;
        }

        public IEnumerable<byte> ToBytes() => shape.ToBytes(shape.Length).Concat(data.ToBytes(data.Length));

        public void AssignFromBytes(ByteReader reader)
        {
            shape = reader.GetIntArray().ToArray();
            data  = reader.GetFloatArray().ToArray();
        }

        public override string ToString() => $"Tensor: {shape.MakeString()} {data.MakeString()}";

        bool Equals(Tensor other) => shape.SequenceEqual(other.shape) && data.SequenceEqual(other.data);

        public override bool Equals(object obj) => obj is Tensor other && Equals(other);

        /// <inheritdoc />
        public IEnumerable<byte> Bytes => shape.ToBytes(shape.Length).Concat(data.ToBytes(data.Length));
    }
}
