using System.Collections.Generic;

namespace RL.NN
{
    public class Identity : Module
    {
        public override IEnumerable<float> Forward(IEnumerable<float> input) => input;
    }
}
