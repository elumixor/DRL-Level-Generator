using System;
using System.Collections.Generic;
using System.Linq;
using Common;
using Common.ByteConversions;

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

    public int AssignFromBytes(byte[] bytes, int startIndex = 0)
    {
        var (s, bytesRead)  = bytes.GetListInt(startIndex);
        var (d, bytesRead2) = bytes.GetListFloat(startIndex + bytesRead);

        shape = s;
        data  = d;

        return bytesRead + bytesRead2;
    }

    public override string ToString() => $"Tensor: {shape.FormString()} {data.FormString()}";

    bool Equals(Tensor other) => shape.SequenceEqual(other.shape) && data.SequenceEqual(other.data);

    public override bool Equals(object obj) => obj is Tensor other && Equals(other);

    public override int GetHashCode() => throw new NotImplementedException();
}
