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
            var cdf_value = Random.Range(0.0f, cdf[p.Length - 1]);
            var index = Array.BinarySearch(cdf, cdf_value);

            if (index < 0) index = ~index; // if not found (probably won't be) BinarySearch returns bitwise complement of next-highest index.

            return index;
        }
    }
}
