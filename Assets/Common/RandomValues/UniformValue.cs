using System;
using UnityEngine;

namespace Common.RandomValues
{
    [Serializable]
    public class UniformValue : IRandomValue
    {
        [SerializeField] float min;
        [SerializeField] float max;

        public UniformValue(float min, float max)
        {
            this.min = min;
            this.max = max;
        }

        /// <inheritdoc/>
        public float Sample => MathExtensions.RandomValue(min, max);
    }

    [Serializable]
    public class UniformValueInt : IRandomValue<int>
    {
        [SerializeField] int min;
        [SerializeField] int max;

        public UniformValueInt(int min, int max)
        {
            this.min = min;
            this.max = max;
        }

        /// <inheritdoc/>
        public int Sample => MathExtensions.RandomValue(min, max);
    }
}
