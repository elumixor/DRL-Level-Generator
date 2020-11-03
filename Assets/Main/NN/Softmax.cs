using System.Collections.Generic;
using Common;

namespace NN
{
    public class Softmax : Module
    {
        public override IEnumerable<float> Forward(IEnumerable<float> x) => x.Softmax();
    }
}
