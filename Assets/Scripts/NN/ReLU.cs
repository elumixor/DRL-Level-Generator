using UnityEngine;

namespace NN {
    public class ReLU : Module {
        public override float[] Forward(float[] input) {
            var length = input.Length;
            var output = new float[length];

            for (var i = 0; i < length; i++) output[i] = Mathf.Clamp01(input[i]);

            return output;
        }
    }
}