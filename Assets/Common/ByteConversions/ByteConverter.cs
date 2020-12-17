using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

// using UnityEngine;

namespace Common.ByteConversions
{
    public static class ByteConverter
    {
        // Generic type
        // public static IEnumerable<byte> ToBytes<T>(this T value) where T : IByteConvertible => value.ToBytes();
        // public static IEnumerable<byte> ToBytes<T>(this IEnumerable<T> value) where T : IByteConvertible =>
        // value.SelectMany(f => f.ToBytes());

        // Basic types
        public static IEnumerable<byte> ToBytes(this float value) => BitConverter.GetBytes(value);

        public static IEnumerable<byte> ToBytes(this int value) => BitConverter.GetBytes(value);

        public static IEnumerable<byte> ToBytes(this bool value) => BitConverter.GetBytes(value);

        public static IEnumerable<byte> ToBytes(this string value)
        {
            var bytes = Encoding.UTF8.GetBytes(value);
            return bytes.Length.ToBytes().Concat(bytes);
        }

        // Unity Vectors
        // public static IEnumerable<byte> ToBytes(this Vector2 value) => value.x.ToBytes().Concat(value.y.ToBytes());
        //
        // public static IEnumerable<byte> ToBytes(this Vector3 value) =>
        //         value.x.ToBytes().Concat(value.y.ToBytes()).Concat(value.z.ToBytes());

        // When transforming enumerable of elements, also include length
        // public static IEnumerable<byte> ToBytes(this IEnumerable<float> enumerable, int length) =>
        // length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));

        public static IEnumerable<byte> ToBytes<T>(this T enumerable)
                where T : IEnumerable<float> =>
                enumerable.SelectMany(e => e.ToBytes());

        public static IEnumerable<byte> ToBytes<T>(this T enumerable, int length)
                where T : IEnumerable<float> =>
                length.ToBytes().Concat(enumerable.ToBytes());

        public static IEnumerable<byte> ToBytes(this IEnumerable<int> enumerable, int length) =>
                length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));

        public static IEnumerable<byte> ToBytes(this IEnumerable<bool> enumerable, int length) =>
                length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));

        // public static IEnumerable<byte> ToBytes(this IEnumerable<Vector2> enumerable, int length) =>
        //         length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));
        //
        // public static IEnumerable<byte> ToBytes(this IEnumerable<Vector3> enumerable, int length) =>
        //         length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));

        public static IEnumerable<byte> MapToBytes<T>(this IReadOnlyCollection<T> collection, Func<T, IEnumerable<byte>> mapping) =>
                collection.Count.ToBytes().Concat(collection.SelectMany(mapping));

        // public static IEnumerable<byte> ToBytes<T>(this IEnumerable<T> enumerable, int length) where T : IByteConvertible =>
        // length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));
    }
}
