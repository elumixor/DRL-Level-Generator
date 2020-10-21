using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace NN {
    public class ReLU : Module {
        public override IEnumerable<float> Forward(IEnumerable<float> input) => input.Select(Mathf.Clamp01);

        public override bool Equals(object obj) {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;
            return obj.GetType() == GetType();
        }

        public override int GetHashCode() => throw new NotImplementedException();
    }
}