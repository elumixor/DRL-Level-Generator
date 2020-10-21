using System.Collections.Generic;
using System.Linq;
using Common;
using UnityEngine;

namespace NN {
    public class Softmax : Module {
        public override IEnumerable<float> Forward(IEnumerable<float> x) => x.Softmax();
    }
}