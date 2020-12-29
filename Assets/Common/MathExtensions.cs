using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using Random = System.Random;

namespace Common
{
    public static class MathExtensions
    {
        // We use custom random not to depend on UnityEngine, and to call from the other threads
        public static readonly Random Random = new Random();
        public static float RandomValue(float min = 0f, float max = 1f) => (float) Random.NextDouble() * (max - min) + min;
        public static int RandomValue(int max) => Random.Next(max);
        public static int RandomValue(int min, int max) => Random.Next(min, max);

        public static T RandomChoice<T>(this IReadOnlyList<T> elements) => elements[RandomValue(elements.Count)];

        public static IEnumerable<T> RandomChoice<T>(this IReadOnlyList<T> elements, int count)
        {
            for (var i = 0; i < count; i++) yield return elements.RandomChoice();
        }

        public static IEnumerable<float> Softmax(this IEnumerable<float> x)
        {
            var input = x.ToArray();
            var max = input.Max();
            for (var i = 0; i < input.Length; i++) input[i] -= max;
            // Debug.Log(input.FormString());
            var length = input.Length;

            var sum = 0f;

            for (var i = 0; i < length; i++) sum += Mathf.Exp(input[i]);
            for (var i = 0; i < length; i++) yield return Mathf.Exp(input[i]) / sum;
        }

        public static int Sample(this IEnumerable<float> probabilities)
        {
            var p = probabilities.ToArray();
            // Sum to create CDF:
            var cdf = new float[p.Length];
            float sum = 0;

            for (var i = 0; i < p.Length; ++i) {
                cdf[i] = sum + p[i];
                sum    = cdf[i];
            }

            // Choose from CDF:
            var max = cdf[p.Length - 1];
            var cdf_value = RandomValue(0.0f, max);
            var index = Array.BinarySearch(cdf, cdf_value);

            if (index < 0)
                index = ~index; // if not found (probably won't be) BinarySearch returns bitwise complement of next-highest index.

            return index;
        }

        public static int ArgMax(this IEnumerable<float> values)
        {
            var index = 0;
            var max = float.NegativeInfinity;

            var i = 0;

            foreach (var value in values) {
                if (value > max) {
                    max   = value;
                    index = i;
                }

                i++;
            }

            return index;
        }

        public static int SampleEpsilonGreedy(this IEnumerable<float> qValues, float epsilon) =>
                RandomValue() < epsilon ? qValues.ArgMax() : RandomValue(0, qValues.Count());

        public static float Mean(this IEnumerable<float> values)
        {
            var count = 0;
            var sum = 0f;

            foreach (var value in values) {
                sum += value;
                count++;
            }

            return sum / count;
        }

        public static float Abs(this float value) => value >= 0 ? value : -value;

        public static float Remap(this float value, float min, float max) => value * (max - min) + min;
    }
}
