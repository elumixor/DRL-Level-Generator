using UnityEngine;

namespace NN {
    public class Softmax : Module {
        public override float[] Forward(float[] input) {
            var length = input.Length;
            var output = new float[length];

            var sum = 0f;

            for (var i = 0; i < length; i++) sum += Mathf.Exp(input[i]);
            for (var i = 0; i < length; i++) output[i] = Mathf.Exp(input[i]) / sum;

            return output;
        }
    }
}