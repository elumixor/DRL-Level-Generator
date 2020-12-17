using System;
using System.Collections.Generic;
using System.Text;
using Common.ByteConversions;

// using UnityEngine;

namespace Common
{
    public class ByteReader
    {
        readonly byte[] bytes;
        int currentOffset;

        public ByteReader(byte[] bytes, int startOffset = 0)
        {
            this.bytes    = bytes;
            currentOffset = startOffset;
        }

        public int ReadInt()
        {
            var result = BitConverter.ToInt32(bytes, currentOffset);
            currentOffset += sizeof(int);
            return result;
        }

        public float ReadFloat()
        {
            var result = BitConverter.ToSingle(bytes, currentOffset);
            currentOffset += sizeof(float);
            return result;
        }

        public string ReadString()
        {
            var length = ReadInt();
            var result = Encoding.UTF8.GetString(bytes, currentOffset, length);
            currentOffset += length;
            return result;
        }

        public T Read<T>()
                where T : IByteAssignable, new()
        {
            var result = new T();
            result.AssignFromBytes(this);
            return result;
        }

        // public Vector2 ToVector2() => new Vector2(ReadFloat(), ReadFloat());
        // public Vector2 ToVector3() => new Vector3(ReadFloat(), ReadFloat(), ReadFloat());

        public IEnumerable<int> GetIntArray()
        {
            var length = ReadInt();

            for (var i = 0; i < length; i++) yield return ReadInt();
        }

        public IEnumerable<float> GetFloatArray()
        {
            var length = ReadInt();

            for (var i = 0; i < length; i++) yield return ReadFloat();
        }

        public IEnumerable<T> GetArray<T>()
                where T : IByteAssignable, new()
        {
            var length = ReadInt();

            for (var i = 0; i < length; i++) {
                var next = new T();
                next.AssignFromBytes(this);
                yield return next;
            }
        }
    }
}
