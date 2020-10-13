using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace Common {
    public static class ByteConverter {
        public static byte[] ToBytes(this float value) => BitConverter.GetBytes(value);
        public static byte[] ToBytes(this bool value) => BitConverter.GetBytes(value);
        public static byte[] ToBytes(this int value) => BitConverter.GetBytes(value);

        public static byte[] ToBytes(this Vector2 value) {
            var result = new byte[2 * sizeof(float)];
            Buffer.BlockCopy(value.x.ToBytes(), 0, result, 0, sizeof(float));
            Buffer.BlockCopy(value.y.ToBytes(), 0, result, sizeof(float), sizeof(float));
            return result;
        }

        public static byte[] ToBytes(this IEnumerable<byte[]> enumerable) => ConcatBytes(enumerable.ToArray());

        public static byte[] ToBytes(this IEnumerable<float> enumerable) => enumerable.Select(e => e.ToBytes()).ToBytes();

        public static byte[] ToBytes<T>(this IEnumerable<T> enumerable, bool writeLength = false) where T : IByteConvertible {
            if (!writeLength) return enumerable.Select(e => e.ToBytes()).ToBytes();
            var arr = enumerable.ToArray();
            return arr.Length.ToBytes().Concat(arr.Select(e => e.ToBytes()).ToBytes()).ToArray();
        }

        public static byte[] ConcatBytes(params byte[][] bytesArrays) {
            var length = bytesArrays.Select(arr => arr.Length).Sum();
            var res = new byte[length];
            var offset = 0;

            foreach (var bytesArray in bytesArrays) {
                var bytesArrayLength = bytesArray.Length;
                Buffer.BlockCopy(bytesArray, 0, res, offset, bytesArrayLength);
                offset += bytesArrayLength;
            }

            return res;
        }


        // bytes -> data
        public static float ToFloat(this byte[] bytes, int startIndex = 0) => BitConverter.ToSingle(bytes, startIndex);
        public static bool ToBool(this byte[] bytes, int startIndex = 0) => BitConverter.ToBoolean(bytes, startIndex);
        public static int ToInt(this byte[] bytes, int startIndex = 0) => BitConverter.ToInt32(bytes, startIndex);
    }
}