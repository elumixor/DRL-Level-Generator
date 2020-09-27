using System;
using System.Collections.Generic;
using System.Linq;

namespace Common {
    public static class ByteConverter {
        public static byte[] ToBytes(this float value) => BitConverter.GetBytes(value);

        public static byte[] ToBytes(this IEnumerable<byte[]> enumerable) => ConcatBytes(enumerable.ToArray());

        public static byte[] ToBytes(this IEnumerable<float> enumerable) => enumerable.Select(e => e.ToBytes()).ToBytes();

        public static byte[] ToBytes<T>(this IEnumerable<T> enumerable) where T : IByteConvertible =>
            enumerable.Select(e => e.ToBytes()).ToBytes();

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
    }
}