using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace NN {
    public class Softmax : Module {
        public override IEnumerable<float> Forward(IEnumerable<float> enumerable) {
            var input = enumerable.ToArray();
            var length = input.Length;

            var sum = 0f;

            for (var i = 0; i < length; i++) sum += Mathf.Exp(input[i]);
            for (var i = 0; i < length; i++) yield return Mathf.Exp(input[i]) / sum;
        }
    }
}