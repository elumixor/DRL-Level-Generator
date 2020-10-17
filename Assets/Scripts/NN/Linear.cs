using UnityEngine;

namespace NN {
    public class Linear : Module {
        readonly int inputSize;
        readonly int outputSize;

        float[] weight;
        float[] bias;

        public Linear(int inputSize, int outputSize) {
            this.inputSize = inputSize;
            this.outputSize = outputSize;

            weight = new float[outputSize * inputSize];
            bias = new float[outputSize];

            for (var i = 0; i < outputSize; i++) {
                for (var j = 0; j < inputSize; j++) weight[i * outputSize + j] = Random.Range(-1f, 1f);
                bias[i] = Random.Range(-1f, 1f);
            }
        }

        public override float[] Forward(float[] input) {
            var output = new float[outputSize];

            for (var i = 0; i < outputSize; i++) {
                var sum = bias[i];
                for (var j = 0; j < inputSize; j++) sum += input[j] * weight[i * outputSize + j];
                output[i] = sum;
            }

            return output;
        }

        public override void LoadStateDict(StateDict stateDict) {
            var (selfParameters, _) = stateDict;

            weight = selfParameters[ModuleParameterName.Weight];
            bias = selfParameters[ModuleParameterName.Bias];
        }
    }
}