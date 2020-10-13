using System;

namespace NN {
    public abstract class Module {
        public abstract float[] Forward(float[] input);
    }
}