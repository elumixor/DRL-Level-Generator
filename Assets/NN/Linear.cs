using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using NN.Configuration;
using Random = UnityEngine.Random;

namespace NN
{
    public class Linear : Module, IFixedOutputLayer
    {
        public int InputSize { get; }
        public int OutputSize { get; }

        float[] bias;
        float[] weight;

        public Linear(int inputSize, int outputSize)
        {
            InputSize  = inputSize;
            OutputSize = outputSize;

            weight = new float[outputSize * inputSize];
            bias   = new float[outputSize];

            for (var i = 0; i < outputSize; i++) {
                for (var j = 0; j < inputSize; j++) weight[i * inputSize + j] = Random.value * 2f - 1f;
                bias[i] = Random.value * 2f - 1f;
            }
        }

        public override StateDict StateDict {
            get {
                var weightTensor = new Tensor(weight, new[] {OutputSize, InputSize});
                var biasTensor = new Tensor(bias, new[] {OutputSize});

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
            for (var i = 0; i < OutputSize; i++) {
                var sum = bias[i];
                for (var j = 0; j < InputSize; j++) sum += x[j] * weight[i * InputSize + j];
                yield return sum;
            }
        }

        public override void SetParameter(ModuleParameterName parameterName, Tensor value)
        {
            switch (parameterName) {
                case ModuleParameterName.bias:
                    if (value.shape[0] != OutputSize)
                        throw new SerializationException("Assigning to bias parameter with a different shape."
                                                       + $"[{OutputSize}] != [{value.shape[0]}]");

                    bias = value.data;
                    break;
                case ModuleParameterName.weight:
                    if (value.shape[0] != OutputSize || value.shape[1] != InputSize)
                        throw new SerializationException("Assigning to weight parameter with a different shape."
                                                       + $" [{OutputSize}, {InputSize}] != [{value.shape[0]}, {value.shape[1]}]");

                    weight = value.data;
                    break;
                default: throw new ArgumentOutOfRangeException(nameof(parameterName), parameterName, null);
            }
        }

        bool Equals(Linear other) =>
                InputSize == other.InputSize && OutputSize == other.OutputSize && weight.SequenceEqual(other.weight)
             && bias.SequenceEqual(other.bias);

        public override bool Equals(object obj)
        {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;

            return obj.GetType() == GetType() && Equals((Linear) obj);
        }

        public override int GetHashCode() => throw new NotImplementedException();
    }
}
