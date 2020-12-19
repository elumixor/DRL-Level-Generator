using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using Random = UnityEngine.Random;

namespace Common
{
    public static class MathExtensions
    {
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
            var cdf_value = Random.Range(0.0f, max);
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
                Random.value < epsilon ? qValues.ArgMax() : Random.Range(0, qValues.Count());

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
