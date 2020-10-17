using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace Common.ByteConversions {
    public static class ByteConverter {
        // Generic type
        public static IEnumerable<byte> ToBytes<T>(this T value) where T : IByteConvertible { return value.ToBytes(); }

        // Basic types
        public static IEnumerable<byte> ToBytes(this float value) { return BitConverter.GetBytes(value); }

        public static IEnumerable<byte> ToBytes(this int value) { return BitConverter.GetBytes(value); }

        public static IEnumerable<byte> ToBytes(this bool value) { return BitConverter.GetBytes(value); }

        // Unity Vectors
        public static IEnumerable<byte> ToBytes(this Vector2 value) { return value.x.ToBytes().Concat(value.y.ToBytes()); }

        public static IEnumerable<byte> ToBytes(this Vector3 value) {
            return value.x.ToBytes().Concat(value.y.ToBytes()).Concat(value.z.ToBytes());
        }

        // When transforming enumerable of elements, also include length
        public static IEnumerable<byte> ToBytes(this IEnumerable<float> enumerable, int length) {
            return length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));
        }

        public static IEnumerable<byte> ToBytes(this IEnumerable<int> enumerable, int length) {
            return length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));
        }

        public static IEnumerable<byte> ToBytes(this IEnumerable<bool> enumerable, int length) {
            return length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));
        }

        public static IEnumerable<byte> ToBytes(this IEnumerable<Vector2> enumerable, int length) {
            return length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));
        }

        public static IEnumerable<byte> ToBytes(this IEnumerable<Vector3> enumerable, int length) {
            return length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));
        }

        public static IEnumerable<byte> ToBytes<T>(this IEnumerable<T> enumerable, int length) where T : IByteConvertible {
            return length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));
        }


        // bytes -> data
        public static float ToFloat(this byte[] bytes, int startIndex = 0) { return BitConverter.ToSingle(bytes, startIndex); }

        public static int ToInt(this byte[] bytes, int startIndex = 0) { return BitConverter.ToInt32(bytes, startIndex); }

        public static bool ToBool(this byte[] bytes, int startIndex = 0) { return BitConverter.ToBoolean(bytes, startIndex); }
    }
}