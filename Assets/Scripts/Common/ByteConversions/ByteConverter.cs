using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;

namespace Common.ByteConversions {
    public static class ByteConverter {
        // Generic type
        public static IEnumerable<byte> ToBytes<T>(this T value) where T : IByteConvertible => value.ToBytes();

        // Basic types
        public static IEnumerable<byte> ToBytes(this float value) => BitConverter.GetBytes(value);

        public static IEnumerable<byte> ToBytes(this int value) => BitConverter.GetBytes(value);

        public static IEnumerable<byte> ToBytes(this bool value) => BitConverter.GetBytes(value);
        public static IEnumerable<byte> ToBytes(this char value) => BitConverter.GetBytes(value);

        public static IEnumerable<byte> ToBytes(this string value) => value.Length.ToBytes().Concat(Encoding.ASCII.GetBytes(value));

        // Unity Vectors
        public static IEnumerable<byte> ToBytes(this Vector2 value) => value.x.ToBytes().Concat(value.y.ToBytes());

        public static IEnumerable<byte> ToBytes(this Vector3 value) =>
            value.x.ToBytes().Concat(value.y.ToBytes()).Concat(value.z.ToBytes());

        // When transforming enumerable of elements, also include length
        public static IEnumerable<byte> ToBytes(this IEnumerable<float> enumerable, int length) =>
            length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));

        public static IEnumerable<byte> ToBytes(this IEnumerable<int> enumerable, int length) =>
            length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));

        public static IEnumerable<byte> ToBytes(this IEnumerable<bool> enumerable, int length) =>
            length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));

        public static IEnumerable<byte> ToBytes(this IEnumerable<Vector2> enumerable, int length) =>
            length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));

        public static IEnumerable<byte> ToBytes(this IEnumerable<Vector3> enumerable, int length) =>
            length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));

        public static IEnumerable<byte> ToBytes<T>(this IEnumerable<T> enumerable, int length) where T : IByteConvertible =>
            length.ToBytes().Concat(enumerable.SelectMany(e => e.ToBytes()));


        // bytes -> data
        public static float ToFloat(this byte[] bytes, int startIndex = 0) => BitConverter.ToSingle(bytes, startIndex);

        public static int ToInt(this byte[] bytes, int startIndex = 0) => BitConverter.ToInt32(bytes, startIndex);

        public static bool ToBool(this byte[] bytes, int startIndex = 0) => BitConverter.ToBoolean(bytes, startIndex);
        public static char ToChar(this byte[] bytes, int startIndex = 0) => BitConverter.ToChar(bytes, startIndex);

        public static (string result, int readCount) GetString(this byte[] bytes, int startIndex = 0) {
            var length = bytes.ToInt(startIndex);
            return (Encoding.ASCII.GetString(bytes, startIndex + sizeof(int), length), length + sizeof(int));
        }

        public static Vector2 ToVector2(this byte[] bytes, int startIndex = 0) =>
            new Vector2(bytes.ToFloat(startIndex), bytes.ToFloat(startIndex + sizeof(float)));

        public static Vector3 ToVector3(this byte[] bytes, int startIndex = 0) =>
            new Vector3(bytes.ToFloat(startIndex), bytes.ToFloat(startIndex + sizeof(float)),
                        bytes.ToFloat(startIndex                            + 2 * sizeof(float)));

        public static (T[] result, int readCount) ToArray<T>(this byte[] bytes, int startIndex = 0) where T : IByteAssignable, new() {
            var length = bytes.ToInt(startIndex);
            var readCount = sizeof(int);

            var result = new T[length];
            for (var i = 0; i < length; i++) {
                result[i] = new T();
                readCount += result[i].AssignFromBytes(bytes, startIndex + readCount);
            }

            return (result, readCount);
        }
    }
}