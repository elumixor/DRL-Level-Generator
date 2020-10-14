using System.Collections.Generic;
using System.Linq;

namespace NN {
    public class Sequential : Module {
        readonly Module[] layers;
        public Sequential(params Module[] layers) => this.layers = layers;

        public override float[] Forward(float[] input) {
            var numLayers = layers.Length;

            for (var i = 0; i < numLayers; i++) input = layers[i].Forward(input);

            return input;
        }

        public override void LoadStateDict(StateDict stateDict) {
            foreach (var (childIndex, childStateDict) in stateDict.childParameters) layers[childIndex].LoadStateDict(childStateDict);
        }
    }
}