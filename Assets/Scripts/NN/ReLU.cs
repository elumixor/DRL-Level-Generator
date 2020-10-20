using System;
using UnityEngine;

namespace NN {
    public class ReLU : Module {
        public override float[] Forward(float[] input) {
            var length = input.Length;
            var output = new float[length];

            for (var i = 0; i < length; i++) output[i] = Mathf.Clamp01(input[i]);

            return output;
        }

        public override bool Equals(object obj) {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;
            return obj.GetType() == GetType();
        }

        public override int GetHashCode() => throw new NotImplementedException();
    }
}