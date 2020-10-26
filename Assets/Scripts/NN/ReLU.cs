using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace NN {
    public class ReLU : Module {
        public override IEnumerable<float> Forward(IEnumerable<float> input) => input.Select(x => Mathf.Max(x, 0));

        public override bool Equals(object obj) {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;
            return obj.GetType() == GetType();
        }
    }
}