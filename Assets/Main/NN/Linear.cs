using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;

namespace NN
{
    public class Linear : Module
    {
        static readonly Random r = new Random();

        readonly int inputSize;
        readonly int outputSize;

        float[] bias;
        float[] weight;

        public Linear(int inputSize, int outputSize)
        {
            this.inputSize  = inputSize;
            this.outputSize = outputSize;

            weight = new float[outputSize * inputSize];
            bias   = new float[outputSize];

            for (var i = 0; i < outputSize; i++) {
                for (var j = 0; j < inputSize; j++) weight[i * inputSize + j] = RandomValue;
                bias[i] = RandomValue;
            }
        }

        static float RandomValue => (float) r.NextDouble() * 2f - 1f;

        public override StateDict StateDict {
            get {
                var weightTensor = new Tensor(weight, new[] {outputSize, inputSize});
                var biasTensor = new Tensor(bias, new[] {outputSize});

                var parameters = new Dictionary<ModuleParameterName, Tensor> {
                        {ModuleParameterName.weight, weightTensor},
                        {ModuleParameterName.bias, biasTensor},
                };

                return new StateDict(parameters);
            }
        }

        // return Random.Range(-1f, 1f);
        public override IEnumerable<float> Forward(IEnumerable<float> input)
        {
            var x = input.ToArray();

            // This is probably the faster version
            for (var i = 0; i < outputSize; i++) {
                var sum = bias[i];
                for (var j = 0; j < inputSize; j++) sum += x[j] * weight[i * inputSize + j];
                yield return sum;
            }
        }

        public override void SetParameter(ModuleParameterName parameterName, Tensor value)
        {
            switch (parameterName) {
                case ModuleParameterName.bias:
                    if (value.shape[0] != outputSize)
                        throw new SerializationException("Assigning to bias parameter with a different shape." + $"[{outputSize}] != [{value.shape[0]}]");

                    bias = value.data;
                    break;
                case ModuleParameterName.weight:
                    if (value.shape[0] != outputSize || value.shape[1] != inputSize)
                        throw new SerializationException("Assigning to weight parameter with a different shape."
                                                       + $" [{outputSize}, {inputSize}] != [{value.shape[0]}, {value.shape[1]}]");

                    weight = value.data;
                    break;
                default: throw new ArgumentOutOfRangeException(nameof(parameterName), parameterName, null);
            }
        }

        bool Equals(Linear other) =>
                inputSize == other.inputSize && outputSize == other.outputSize && weight.SequenceEqual(other.weight) && bias.SequenceEqual(other.bias);

        public override bool Equals(object obj)
        {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;

            return obj.GetType() == GetType() && Equals((Linear) obj);
        }

        public override int GetHashCode() => throw new NotImplementedException();
    }
}
