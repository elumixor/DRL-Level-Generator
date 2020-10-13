using UnityEngine;

namespace NN {
    public class Linear : Module {
        readonly int inputSize;
        readonly int outputSize;

        float[][] W;
        float[] b;
        
        public Linear(int inputSize, int outputSize) {
            this.inputSize = inputSize;
            this.outputSize = outputSize;
            
            W = new float[outputSize][];
            b = new float[outputSize];

            for (var i = 0; i < outputSize; i++) {
                W[i] = new float[inputSize];
                for (var j = 0; j < inputSize; j++) W[i][j] = Random.Range(-1f, 1f);
                b[i] = Random.Range(-1f, 1f);
            }
        }

        public override float[] Forward(float[] input) {
            var output = new float[outputSize];

            for (var i = 0; i < outputSize; i++) {
                var sum = b[i];
                for (var j = 0; j < inputSize; j++) sum += input[j] * W[i][j];
                output[i] = sum;
            }
            
            return output;
        }
    }
}